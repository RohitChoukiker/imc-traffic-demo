# 🚦 Smart City Indore – AI Chatbot (RAG-based)

An AI-powered chatbot built for Smart City Indore, designed to assist citizens by answering queries using government data.

This project leverages Retrieval-Augmented Generation (RAG) to provide accurate, context-aware responses from large-scale datasets.

---

##  Overview

This system is a full-stack AI application that enables users to interact with government-related data through a conversational interface.

- Chat-based interface for citizens
- Handles large datasets (~80K+ rows)
- Fast and scalable backend APIs
- Context-aware responses using RAG

---

##  Tech Stack

### Backend
- FastAPI
- LangChain
- RAG (Retrieval-Augmented Generation)
- Anthropic (Claude / LLM)

### Frontend
- React.js

### Data Processing
- Large dataset handling (~80,000+ records)
- Vector embeddings for semantic search

---

##  Features

- Semantic search over government datasets
- AI-powered chatbot using RAG pipeline
- Efficient handling of large-scale data (80K+ rows)
- Fast API responses using FastAPI
- Modular architecture (easy to scale)

---

##  How It Works

1. Data is preprocessed and converted into embeddings
2. Stored in a vector database
3. User query is converted into embedding
4. Relevant data chunks are retrieved
5. Passed to LLM (Anthropic) for response generation

---

##  Installation

### Backend

cd backend  
pip install -r requirements.txt  
uvicorn main:app --reload  

### Frontend

cd frontend  
npm install  
npm run dev 

---

##  Data Handling

- Processed 80,000+ rows of government data  
- Chunking + embedding used for efficient retrieval  
- Optimized for fast query response  

---

##  Use Case

- Smart City services assistance  
- Government data accessibility  
- Citizen query resolution  
- Public service automation  

---

##  Future Improvements

- Multi-language support  
- Voice-based interaction  
- Real-time data integration  
- Admin dashboard for analytics  

---

## Author

Rohit Choukiker

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and support!
EOF
