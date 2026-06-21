import json
import yaml
from pathlib import Path
from typing import Dict, List, Any

class CodeParser:
    LANGUAGES = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.go': 'go',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
    }
    
    def __init__(self):
        self.parsers = {}
    
    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        ext = file_path.suffix.lower()
        
        if ext in ['.py', '.js', '.ts', '.go', '.java']:
            return self._parse_code_file(file_path, ext)
        elif ext in ['.md', '.rst', '.txt']:
            return self._parse_documentation(file_path)
        elif ext in ['.yaml', '.yml', '.json']:
            return self._parse_api_spec(file_path)
        else:
            return self._parse_text_file(file_path)
    
    def _parse_code_file(self, file_path: Path, ext: str) -> Dict[str, Any]:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        functions = self._extract_functions(content, ext)
        classes = self._extract_classes(content, ext)
        imports = self._extract_imports(content, ext)
        
        return {
            'type': 'code',
            'path': str(file_path),
            'language': self.LANGUAGES.get(ext, 'unknown'),
            'content': content,
            'functions': functions,
            'classes': classes,
            'imports': imports,
            'metadata': {
                'size': len(content),
                'lines': content.count('\n')
            }
        }
    
    def _extract_functions(self, content: str, ext: str) -> List[Dict]:
        functions = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if ext == '.py' and line.strip().startswith('def '):
                func_name = line.strip()[4:].split('(')[0]
                functions.append({
                    'name': func_name,
                    'line': i + 1,
                    'signature': line.strip()
                })
            elif ext in ['.js', '.ts'] and 'function' in line:
                if 'function ' in line:
                    func_name = line.split('function ')[1].split('(')[0].split('{')[0].strip()
                    functions.append({
                        'name': func_name,
                        'line': i + 1,
                        'signature': line.strip()
                    })
        
        return functions
    
    def _extract_classes(self, content: str, ext: str) -> List[Dict]:
        classes = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if ext == '.py' and line.strip().startswith('class '):
                class_name = line.strip()[6:].split(':')[0].split('(')[0]
                classes.append({
                    'name': class_name,
                    'line': i + 1,
                    'signature': line.strip()
                })
            elif ext == '.java' and 'class ' in line and '{' in line:
                parts = line.split('class ')
                if len(parts) > 1:
                    class_name = parts[1].split('{')[0].split(' ')[0].strip()
                    classes.append({
                        'name': class_name,
                        'line': i + 1,
                        'signature': line.strip()
                    })
        
        return classes
    
    def _extract_imports(self, content: str, ext: str) -> List[str]:
        imports = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if ext == '.py' and line.startswith('import '):
                imports.append(line[7:])
            elif ext == '.py' and line.startswith('from '):
                imports.append(line)
            elif ext == '.js' and 'require(' in line:
                imports.append(line)
            elif ext == '.go' and line.startswith('import '):
                imports.append(line)
        
        return imports
    
    def _parse_documentation(self, file_path: Path) -> Dict[str, Any]:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        headings = []
        lines = content.split('\n')
        for line in lines:
            if line.startswith('#'):
                level = len(line.split(' ')[0])
                title = line.lstrip('#').strip()
                headings.append({'level': level, 'title': title})
        
        return {
            'type': 'documentation',
            'path': str(file_path),
            'format': file_path.suffix[1:],
            'content': content,
            'headings': headings,
            'metadata': {
                'size': len(content),
                'lines': len(lines)
            }
        }
    
    def _parse_api_spec(self, file_path: Path) -> Dict[str, Any]:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        endpoints = []
        if file_path.suffix == '.json':
            data = json.loads(content)
            if 'paths' in data:
                for path, methods in data['paths'].items():
                    for method, details in methods.items():
                        endpoints.append({
                            'path': path,
                            'method': method.upper(),
                            'description': details.get('description', ''),
                            'summary': details.get('summary', '')
                        })
        elif file_path.suffix in ['.yaml', '.yml']:
            data = yaml.safe_load(content)
            if 'paths' in data:
                for path, methods in data['paths'].items():
                    for method, details in methods.items():
                        endpoints.append({
                            'path': path,
                            'method': method.upper(),
                            'description': details.get('description', ''),
                            'summary': details.get('summary', '')
                        })
        
        return {
            'type': 'api_spec',
            'path': str(file_path),
            'content': content,
            'endpoints': endpoints,
            'metadata': {
                'endpoint_count': len(endpoints)
            }
        }
    
    def _parse_text_file(self, file_path: Path) -> Dict[str, Any]:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        return {
            'type': 'text',
            'path': str(file_path),
            'content': content,
            'metadata': {'size': len(content)}
        }
