#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from assistant import RAGAssistant

def main():
    parser = argparse.ArgumentParser(description="Ingest a code repository")
    parser.add_argument("repo_path", type=str, help="Path to the repository")
    parser.add_argument("--clear", action="store_true", help="Clear existing data")
    
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path)
    if not repo_path.exists():
        print(f" Error: Path {repo_path} does not exist")
        sys.exit(1)
    
    assistant = RAGAssistant()
    
    if args.clear:
        print("Clearing existing vector database...")
        assistant.vector_store.delete_all()
    
    try:
        assistant.ingest_repository(str(repo_path))
        print("\n Ingestion completed successfully!")
    except Exception as e:
        print(f"\n Error during ingestion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
