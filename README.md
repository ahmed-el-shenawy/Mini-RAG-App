# Mini-RAG

A lightweight **Retrieval-Augmented Generation (RAG)** pipeline built with Python.
This project demonstrates how to combine **embeddings**, **vector search**, and a **Large Language Model (LLM)** to answer questions based on your own documents.

---

## 🚀 Features
- Ingest and preprocess text documents
- Generate embeddings using state-of-the-art models
- Store vectors in a local vector database
- Retrieve relevant chunks for a given query
- Pass context to an LLM to generate accurate answers
- Minimal, easy-to-extend codebase

---

## 📋 Requirements
- **Python 3.12.3**
- Recommended: [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

---

## 🛠 Installation with Miniconda

```bash
# 1. Install Miniconda (Ubuntu/Linux)
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc

# 2. Create a conda environment
conda create -n mini-rag-app python=3.12.3 -y

# 3. Activate the environment
conda activate mini-rag-app

# 4. Install project dependencies
pip install -r requirements.txt
