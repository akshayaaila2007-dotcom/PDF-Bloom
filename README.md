# 📖 PDF Bloom

An AI-powered PDF question-answering application that lets you upload a PDF and ask questions about its content.

https://pdf-bloom-xcpajts6xkpzgnecghdyp8.streamlit.app/

## ✨ Features

- 📂 Upload PDF documents
- 🔎 Search relevant information from the document
- 💡 Ask questions about your PDF
- 🤖 Gemini AI generates answers using the retrieved content
- 🧠 ChromaDB stores document embeddings for semantic search
- ⚡ Simple and interactive Streamlit interface
- 📚 View the document sections used to generate an answer

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- ChromaDB
- PyPDF
- python-dotenv

## 🔄 How It Works

```text
Upload PDF
    ↓
Extract PDF text
    ↓
Split text into sections
    ↓
Create embeddings
    ↓
Store embeddings in ChromaDB
    ↓
Ask a question
    ↓
Find relevant sections
    ↓
Gemini generates the answer
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/akshayaaila2007-dotcom/PDF-Bloom.git
cd PDF-Bloom
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key_here
```

**Never upload your `.env` file or API key to GitHub.**

### 4. Run the application

```bash
streamlit run app.py
```

## 🌐 Live Application

The application is deployed using Streamlit Community Cloud.

## 📌 Project Purpose

PDF Bloom was created to explore Retrieval-Augmented Generation (RAG), semantic search, vector databases, and AI-powered document question answering.

## 👩‍💻 Author

**Akshaya**

CSE (AI & ML) Student

GitHub: [akshayaaila2007-dotcom](https://github.com/akshayaaila2007-dotcom)
