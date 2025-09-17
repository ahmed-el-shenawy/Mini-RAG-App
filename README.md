# Mini-RAG-App

A lightweight **Retrieval-Augmented Generation (RAG)** pipeline built with Python.
This project demonstrates how to combine **embeddings**, **vector search**, and a **Large Language Model (LLM)** to answer questions based on your own documents.

---

## 🚀 Features
- Ingest and preprocess your data
- Generate embeddings using state-of-the-art models
- Store vectors in a local vector database
- Retrieve relevant chunks for a given query
- Pass context to an LLM to generate accurate answers
- Minimal, easy-to-extend codebase

---

## 📋 Requirements
- **Python 3.12.3**
- **Miniconda**

---

## 🛠 Installation with Miniconda
### 1. Install Miniconda (Ubuntu/Linux)
```bash
cd ~
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc

```
### 💻 Windows users
- First install WSL → [Microsoft guide](https://learn.microsoft.com/en-us/windows/wsl/install)
- Then install Miniconda inside WSL using the Linux instructions above.
- 🎥 Helpful video: [Install Miniconda on Windows with WSL](https://www.youtube.com/watch?v=ujKNOYKi88A)

### 2. Create a conda environment
```bash
conda create -n mini-rag-app python=3.12.3 -y
```
### 3. Activate the environment
```bash
conda activate mini-rag-app
```
### 4. Install project dependencies
```bash
pip install -r requirements.txt
```
## 🎨 (Optional) Customize the Terminal Prompt
```bash
export PS1='$(if [ -n "$CONDA_DEFAULT_ENV" ]; then echo -n "(\[\e[1;33m\]$CONDA_DEFAULT_ENV\[\e[0m\]) "; fi)\[\e[1;32m\]\u@\h\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]\n$ '
```
