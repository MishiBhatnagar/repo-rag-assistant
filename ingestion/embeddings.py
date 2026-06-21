from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import hashlib

class EmbeddingGenerator:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        print(f"Model loaded. Embedding dimension: {self.dimension}")
    
    def generate_embeddings(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        texts = [chunk['content'] for chunk in chunks]
        
        print(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        for chunk, embedding in zip(chunks, embeddings):
            chunk['embedding'] = embedding.tolist()
            chunk['id'] = hashlib.md5(f"{chunk['file_path']}{chunk['content'][:100]}".encode()).hexdigest()
        
        return chunks
    
    def embed_query(self, query: str) -> np.ndarray:
        return self.model.encode([query])[0]
