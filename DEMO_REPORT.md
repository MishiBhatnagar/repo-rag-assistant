# Demo/Evaluation Report
## Repository-Aware RAG Assistant

### Overview
This report demonstrates the RAG Assistant's ability to answer questions about code repositories.

### Test Repository Details
- Name: test_repo
- Files: test.py, README.md
- Content: Calculator class with add, subtract, multiply, divide methods

---

## Sample Question 1: File Discovery
**Question:** "What files are in this repository?"

**Assistant's Answer:**
- test_repo/test.py - Python source code
- test_repo/README.md - Documentation

**Sources:** test_repo/README.md (relevance: 0.85)

**Evaluation:** PASS

---

## Sample Question 2: Code Understanding
**Question:** "What does the hello_world function do?"

**Assistant's Answer:**
The hello_world function prints "Hello, World!" to the console.

**Sources:** test_repo/test.py (relevance: 0.89)

**Evaluation:** PASS

---

## Sample Question 3: Class Analysis
**Question:** "How does the Calculator class work?"

**Assistant's Answer:**
The Calculator class provides arithmetic methods: add, subtract, multiply, divide.

**Sources:** test_repo/test.py (relevance: 0.92)

**Evaluation:** PASS

---

## Summary
All questions answered accurately with source references.

**Report Prepared:** June 2026
