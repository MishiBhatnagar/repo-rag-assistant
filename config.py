import os
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Config:
    # Paths
    REPO_PATH: Path = Path("./sample_repo")
    VECTOR_DB_PATH: Path = Path("./vector_db")
    
    # Embedding settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384
    
    # Chunking settings
    MAX_CHUNK_SIZE: int = 1500
    MIN_CHUNK_SIZE: int = 100
    CHUNK_OVERLAP: int = 200
    
    # Retrieval settings
    TOP_K_SEMANTIC: int = 5
    TOP_K_KEYWORD: int = 3
    SIMILARITY_THRESHOLD: float = 0.7
    
    # File patterns
    INCLUDE_PATTERNS: list = None
    EXCLUDE_PATTERNS: list = None
    
    def __post_init__(self):
        if self.INCLUDE_PATTERNS is None:
            self.INCLUDE_PATTERNS = [
                "*.py", "*.js", "*.ts", "*.go", "*.java",
                "*.md", "*.rst", "*.txt",
                "*.yaml", "*.yml", "*.json"
            ]
        if self.EXCLUDE_PATTERNS is None:
            self.EXCLUDE_PATTERNS = [
                "*.pyc", "__pycache__", "*.log",
                "node_modules", ".git", ".venv", "venv"
            ]

config = Config()
