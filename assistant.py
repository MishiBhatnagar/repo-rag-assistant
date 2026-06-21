import sys
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
import os

sys.path.append(str(Path(__file__).parent))

from config import config
from ingestion.parser import CodeParser
from ingestion.chunker import SyntaxAwareChunker
from ingestion.embeddings import EmbeddingGenerator
from retrieval.vector_store import VectorStore
from retrieval.hybrid_search import HybridSearch
from retrieval.prompt_builder import PromptBuilder

class RAGAssistant:
    def __init__(self):
        print("Initializing RAG Assistant...")
        self.parser = CodeParser()
        self.chunker = SyntaxAwareChunker(
            max_chunk_size=config.MAX_CHUNK_SIZE,
            overlap=config.CHUNK_OVERLAP
        )
        self.embedder = EmbeddingGenerator(config.EMBEDDING_MODEL)
        self.vector_store = VectorStore(str(config.VECTOR_DB_PATH))
        self.hybrid_search = HybridSearch(self.vector_store)
        self.prompt_builder = PromptBuilder()
        self.llm = self._setup_llm()
        print("RAG Assistant ready!")
    
    def _setup_llm(self):
        try:
            from local_llm import OllamaLLM
            print("Attempting to connect to Ollama...")
            llm = OllamaLLM()
            test_response = llm.generate("test")
            if "Error" not in test_response:
                print("Using Ollama (local LLM)")
                return llm
            else:
                print(f"Ollama test failed: {test_response}")
        except Exception as e:
            print(f"Ollama not available: {e}")
        
        print("Using MockLLM (fallback)")
        return MockLLM()
    
    def ingest_repository(self, repo_path: str):
        repo_path = Path(repo_path)
        if not repo_path.exists():
            raise ValueError(f"Repository path not found: {repo_path}")
        
        print(f"\nIngesting repository: {repo_path}")
        all_chunks = []
        files_processed = 0
        
        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and self._should_process(file_path):
                try:
                    parsed = self.parser.parse_file(file_path)
                    chunks = self.chunker.chunk_parsed_file(parsed)
                    
                    for chunk in chunks:
                        chunk['file_path'] = str(file_path)
                    
                    all_chunks.extend(chunks)
                    files_processed += 1
                    
                    if files_processed % 10 == 0:
                        print(f"  Processed {files_processed} files...")
                
                except Exception as e:
                    print(f"  Error processing {file_path}: {e}")
        
        print(f"Processed {files_processed} files, generated {len(all_chunks)} chunks")
        
        print("Generating embeddings...")
        chunked_with_embeddings = self.embedder.generate_embeddings(all_chunks)
        
        print("Storing in vector database...")
        self.vector_store.add_chunks(chunked_with_embeddings)
        
        print("Building keyword index...")
        self.hybrid_search.build_keyword_index(chunked_with_embeddings)
        
        print(f"Ingestion complete. Total chunks: {self.vector_store.count()}")
    
    def _should_process(self, file_path: Path) -> bool:
        included = False
        for pattern in config.INCLUDE_PATTERNS:
            if file_path.match(pattern):
                included = True
                break
        
        if not included:
            return False
        
        for pattern in config.EXCLUDE_PATTERNS:
            if file_path.match(pattern) or pattern in str(file_path):
                return False
        
        return True
    
    def ask(self, question: str) -> str:
        print(f"\nQuestion: {question}")
        
        query_embedding = self.embedder.embed_query(question)
        
        retrieved = self.hybrid_search.search(
            question,
            query_embedding.tolist(),
            top_k=config.TOP_K_SEMANTIC
        )
        
        if not retrieved:
            return "No relevant information found in the repository."
        
        print(f"Retrieved {len(retrieved)} relevant chunks")
        
        prompt = self.prompt_builder.build_prompt(question, retrieved)
        
        print("Generating response with LLM...")
        answer = self.llm.generate(prompt)
        
        sources = self._format_sources(retrieved)
        full_answer = f"{answer}\n\n{sources}"
        
        return full_answer
    
    def _format_sources(self, retrieved: List[Dict]) -> str:
        sources = []
        for i, chunk in enumerate(retrieved[:3], 1):
            file_path = chunk.get('metadata', {}).get('file_path', 'unknown')
            similarity = chunk.get('similarity_score', 0)
            sources.append(f"{i}. {file_path} (relevance: {similarity:.2f})")
        
        return f"\n**Sources:**\n" + "\n".join(sources)

class MockLLM:
    def generate(self, prompt: str) -> str:
        return """Based on the code context provided, here's what I found:

[This is a mock response. In production, this would be replaced with actual LLM output from OpenAI, Anthropic, or a local model.]

The context shows relevant code snippets and documentation that address your question.

To get accurate answers, please:
1. Set up your preferred LLM (OpenAI, Anthropic, or local)
2. Update the _setup_llm() method in RAGAssistant class
3. Install the required LLM dependencies"""
