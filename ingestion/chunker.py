from typing import List, Dict, Any
import re

class SyntaxAwareChunker:
    def __init__(self, max_chunk_size: int = 1500, overlap: int = 200):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
    
    def chunk_parsed_file(self, parsed_file: Dict[str, Any]) -> List[Dict[str, Any]]:
        file_type = parsed_file['type']
        
        if file_type == 'code':
            return self._chunk_code(parsed_file)
        elif file_type == 'documentation':
            return self._chunk_documentation(parsed_file)
        elif file_type == 'api_spec':
            return self._chunk_api_spec(parsed_file)
        else:
            return self._chunk_text(parsed_file)
    
    def _chunk_code(self, parsed_file: Dict[str, Any]) -> List[Dict[str, Any]]:
        chunks = []
        content = parsed_file['content']
        lines = content.split('\n')
        
        # Chunk by functions
        for func in parsed_file.get('functions', []):
            start = func['line'] - 1
            end = min(start + 50, len(lines))
            chunk_content = '\n'.join(lines[start:end])
            
            if len(chunk_content) <= self.max_chunk_size:
                chunks.append({
                    'content': chunk_content,
                    'type': 'function',
                    'name': func['name'],
                    'file_path': parsed_file['path'],
                    'language': parsed_file['language'],
                    'metadata': {'chunk_type': 'function'}
                })
        
        # If no functions, chunk by paragraphs
        if not chunks:
            chunks = self._chunk_by_paragraphs(lines, parsed_file)
        
        return chunks
    
    def _chunk_by_paragraphs(self, lines: List[str], parsed_file: Dict) -> List[Dict]:
        chunks = []
        current_chunk = []
        current_size = 0
        
        for i, line in enumerate(lines):
            line_size = len(line)
            
            if (line.strip() == '' or current_size + line_size > self.max_chunk_size) and current_chunk:
                chunks.append({
                    'content': '\n'.join(current_chunk),
                    'type': 'paragraph',
                    'file_path': parsed_file['path'],
                    'language': parsed_file.get('language', 'text'),
                    'metadata': {'chunk_type': 'paragraph'}
                })
                current_chunk = []
                current_size = 0
            
            current_chunk.append(line)
            current_size += line_size
        
        if current_chunk:
            chunks.append({
                'content': '\n'.join(current_chunk),
                'type': 'paragraph',
                'file_path': parsed_file['path'],
                'language': parsed_file.get('language', 'text'),
                'metadata': {'chunk_type': 'paragraph'}
            })
        
        return chunks
    
    def _chunk_documentation(self, parsed_file: Dict) -> List[Dict]:
        chunks = []
        content = parsed_file['content']
        
        # Split by double newlines
        sections = re.split(r'\n\s*\n', content)
        for i, section in enumerate(sections):
            if section.strip():
                chunks.append({
                    'content': section.strip(),
                    'type': 'section',
                    'file_path': parsed_file['path'],
                    'format': parsed_file['format'],
                    'metadata': {'chunk_type': 'section', 'index': i}
                })
        
        return chunks
    
    def _chunk_api_spec(self, parsed_file: Dict) -> List[Dict]:
        chunks = []
        
        for endpoint in parsed_file.get('endpoints', []):
            chunk_content = f"""Endpoint: {endpoint['method']} {endpoint['path']}
Description: {endpoint.get('description', '')}"""
            
            chunks.append({
                'content': chunk_content,
                'type': 'endpoint',
                'file_path': parsed_file['path'],
                'metadata': {
                    'chunk_type': 'api_endpoint',
                    'method': endpoint['method'],
                    'path': endpoint['path']
                }
            })
        
        return chunks
    
    def _chunk_text(self, parsed_file: Dict) -> List[Dict]:
        content = parsed_file['content']
        chunks = []
        
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', content)
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            if current_size + len(sentence) > self.max_chunk_size and current_chunk:
                chunks.append({
                    'content': ' '.join(current_chunk),
                    'type': 'text',
                    'file_path': parsed_file['path'],
                    'metadata': {'chunk_type': 'text_segment'}
                })
                current_chunk = []
                current_size = 0
            
            current_chunk.append(sentence)
            current_size += len(sentence)
        
        if current_chunk:
            chunks.append({
                'content': ' '.join(current_chunk),
                'type': 'text',
                'file_path': parsed_file['path'],
                'metadata': {'chunk_type': 'text_segment'}
            })
        
        return chunks
