from typing import List, Dict, Any

class PromptBuilder:
    def build_prompt(self, query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
        # Format context
        context_parts = []
        for i, chunk in enumerate(retrieved_chunks[:5], 1):
            file_path = chunk.get('metadata', {}).get('file_path', 'unknown')
            context_parts.append(f"[Context {i}] From {file_path}:\n{chunk['content'][:1000]}")
        
        context = "\n\n".join(context_parts)
        
        prompt = f"""You are a code repository assistant. Answer questions based on the provided code context.

CONTEXT:
{context}

QUESTION: {query}

INSTRUCTIONS:
1. Answer based ONLY on the context above
2. If the context doesn't have enough info, say so
3. Mention specific file paths when referencing code
4. Be concise but thorough

ANSWER:"""
        
        return prompt
