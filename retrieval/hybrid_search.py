from typing import List, Dict, Any
import re
from rank_bm25 import BM25Okapi

class HybridSearch:
    def __init__(self, vector_store, weight_semantic: float = 0.7, weight_keyword: float = 0.3):
        self.vector_store = vector_store
        self.weight_semantic = weight_semantic
        self.weight_keyword = weight_keyword
        self.bm25_index = None
        self.all_chunks = []
    
    def build_keyword_index(self, chunks: List[Dict[str, Any]]):
        self.all_chunks = chunks
        tokenized_chunks = [self._tokenize(chunk['content']) for chunk in chunks]
        self.bm25_index = BM25Okapi(tokenized_chunks)
        print(f"Built keyword index with {len(chunks)} documents")
    
    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b[a-zA-Z0-9_]+\b', text.lower())
    
    def search(self, query: str, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        semantic_results = self.vector_store.search(query_embedding, top_k=top_k * 2)
        
        if self.bm25_index and self.all_chunks:
            tokenized_query = self._tokenize(query)
            bm25_scores = self.bm25_index.get_scores(tokenized_query)
            
            for result in semantic_results:
                result['keyword_score'] = 0
                for i, chunk in enumerate(self.all_chunks):
                    if chunk['id'] == result['id']:
                        max_bm25 = max(bm25_scores) if bm25_scores else 1
                        result['keyword_score'] = bm25_scores[i] / max_bm25 if max_bm25 > 0 else 0
                        break
                
                result['combined_score'] = (
                    self.weight_semantic * result['similarity_score'] +
                    self.weight_keyword * result.get('keyword_score', 0)
                )
            
            semantic_results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return semantic_results[:top_k]
