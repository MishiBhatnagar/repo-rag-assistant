import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, persist_directory: str = "./vector_db"):
        # Updated for newer ChromaDB versions
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False
            )
        )
        
        self.collection = self.client.get_or_create_collection(
            name="code_chunks",
            metadata={"hnsw:space": "cosine"}
        )
        print(f"Vector store initialized at {persist_directory}")
    
    def add_chunks(self, chunks: List[Dict[str, Any]]):
        if not chunks:
            return
        
        ids = [chunk['id'] for chunk in chunks]
        embeddings = [chunk['embedding'] for chunk in chunks]
        documents = [chunk['content'] for chunk in chunks]
        metadatas = [self._extract_metadata(chunk) for chunk in chunks]
        
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            self.collection.add(
                ids=ids[i:i+batch_size],
                embeddings=embeddings[i:i+batch_size],
                documents=documents[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size]
            )
        
        print(f"Added {len(chunks)} chunks to vector store")
    
    def _extract_metadata(self, chunk: Dict[str, Any]) -> Dict[str, Any]:
        metadata = {
            'file_path': chunk.get('file_path', ''),
            'type': chunk.get('type', 'unknown'),
            'chunk_type': chunk.get('metadata', {}).get('chunk_type', 'unknown')
        }
        
        if 'name' in chunk:
            metadata['entity_name'] = chunk['name']
        if 'heading' in chunk:
            metadata['heading'] = chunk['heading']
        
        return metadata
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        formatted_results = []
        if results['ids'] and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'similarity_score': 1 - results['distances'][0][i]
                })
        
        return formatted_results
    
    def delete_all(self):
        try:
            self.client.delete_collection("code_chunks")
            self.collection = self.client.create_collection("code_chunks")
            print("Vector store cleared")
        except Exception as e:
            print(f"Error clearing vector store: {e}")
    
    def count(self) -> int:
        return self.collection.count()
