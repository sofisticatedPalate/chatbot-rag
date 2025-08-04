# Intelligent Chatbot with RAG for Company Documentation
## 🚀 Project Overview
This project demonstrates an Intelligent Chatbot powered by Retrieval Augmented Generation (RAG), designed to answer questions using your company's internal documentation (specifically, an Obsidian vault of Markdown files). This chatbot enhances the capabilities of Large Language Models (LLMs) by providing them with specific, up-to-date context from your knowledge base, significantly reducing hallucinations and enabling accurate answers to domain-specific queries.

It's an excellent showcase of practical AI and LLM application development, ideal for a technical portfolio.

## ✨ Features
- Contextual Question Answering: Answers user queries based only on the provided company documentation.
- Obsidian Vault Integration: Seamlessly loads Markdown notes from an Obsidian vault.
- Markdown-Aware Chunking: Utilizes MarkdownHeaderTextSplitter to preserve document structure during text processing.
- Vector Database for Efficient Retrieval: Stores document embeddings in ChromaDB for fast and relevant context retrieval.
- Google Gemini Integration: Leverages Google's powerful Gemini LLM for generating responses.
- Streamlit User Interface: Provides an interactive and user-friendly web interface for chatbot interaction.
- Modular Codebase: Organized into separate files for data ingestion, core chatbot logic, and the UI, promoting readability and maintainability.

🛠️ Technologies Used
- Python 3.x
- LangChain: For orchestrating the RAG pipeline (document loading, splitting, retrieval, LLM integration).
- LangChain Community: Specific loaders and integrations (e.g., ObsidianLoader, HuggingFaceEmbeddings).
- ChromaDB: Lightweight, in-memory vector database for storing and querying document embeddings.
- HuggingFace Transformers/Embeddings: For generating high-quality text embeddings.
- Google Generative AI (Gemini): The Large Language Model used for generating answers.
- Streamlit: For building the interactive web application.
- os module: For file system operations (e.g., checking for database existence).

📂 Project Structure
```
.
├── data/
│   └── # (Optional) You might place sample documentation here, or point directly to your Obsidian vault
├── .env                  # Stores API keys (ignored by Git)
├── requirements.txt      # Python dependencies
├── ingest_data.py        # Script to load, chunk, embed documents, and build the vector database
├── chatbot_logic.py      # Contains the core RAG chain setup and LLM integration
├── app.py                # The Streamlit web application for the chatbot UI
└── README.md             # This file
```

## 🚀 Getting Started
Follow these steps to set up and run the chatbot on your local machine.

### Prerequisites
- Python 3.8+ installed.
- A Google API Key for Gemini. You can obtain one from the Google AI Studio.

### 1. Clone the Repository
```
git clone [YOUR_GITHUB_REPO_URL]
cd [your-repo-name]
```
### 2. Set Up Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.
```
python -m venv rag_env
source rag_env/bin/activate  # On macOS/Linux
# .\rag_env\Scripts\activate  # On Windows
```
### 3. Install Dependencies
Install all required Python packages:
```
pip install -r requirements.txt
```
### 4. Configure API Key
Create a .env file in the root of your project directory and add your Google API Key:
```
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
```
Important: Never commit your .env file to version control. It's already included in the .gitignore for your safety.

### 5. Prepare Your Documentation (Ingestion Step)
This step processes your Obsidian vault and creates the vector database that the chatbot will use.

Before running:
- Update ingest_data.py: Open ingest_data.py and replace "/path/to/your/Obsidian/Vault" with the absolute path to your Obsidian vault.

Now, run the ingestion script:
```
python ingest_data.py
```
This will create a ./chroma_db directory in your project root, containing your vectorized documentation. This step only needs to be run once, or whenever your documentation changes significantly.

### 6. Launch the Chatbot Application
Once the chroma_db directory has been successfully created by ingest_data.py, you can launch the Streamlit application:
```
streamlit run app.py
```
Your chatbot application should open in your default web browser (usually at http://localhost:8501).

## 💡 Usage
Once the Streamlit app is running:

1. Type your questions related to your company documentation into the chat input box.
2. Press Enter, and the chatbot will retrieve relevant information from your Obsidian vault and generate a grounded answer.
3. The chatbot will also display the source documents it used to formulate its answer, if return_source_documents=True is enabled in chatbot_logic.py.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

[Your Name/GitHub Username]
[Link to your GitHub Profile (Optional)]