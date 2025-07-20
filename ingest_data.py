import os
from langchain_community.document_loaders import ObsidianLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- Configuration ---
# IMPORTANT: Replace with the actual path to your Obsidian vault
OBSIDIAN_VAULT_PATH = "/Users/mds/mds_obsidian"
CHROMA_DB_DIR = "./chroma_db"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def ingest_documents():
    """
    Loads documents from the Obsidian vault, splits them into chunks,
    creates embeddings, and stores them in a ChromaDB vector store.
    """
    print(f"Starting document ingestion from: {OBSIDIAN_VAULT_PATH}")

    # 1. Load Documents using ObsidianLoader
    try:
        # ObsidianLoader directly loads documents as langchain_core.documents.base.Document objects
        # The 'path' argument should point to the root of your Obsidian vault.
        loader = ObsidianLoader(OBSIDIAN_VAULT_PATH)
        documents = loader.load()
        print(f"Loaded {len(documents)} documents from Obsidian vault.")
        if not documents:
            print("No documents loaded. Please check your OBSIDIAN_VAULT_PATH and ensure it contains Markdown files.")
            return
    except Exception as e:
        print(f"Error loading documents from Obsidian vault: {e}")
        print("Please ensure 'pip install langchain-community' is done and the vault path is correct.")
        return

    # 2. Split Documents into Chunks
    # Using MarkdownHeaderTextSplitter for structured Markdown splitting
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
        ("#####", "Header 5"),
        ("######", "Header 6"),
    ]

    # Process each document's page_content with MarkdownHeaderTextSplitter
    all_chunks = []
    for i, doc in enumerate(documents):
        try:
            markdown_splitter = MarkdownHeaderTextSplitter(
                headers_to_split_on=headers_to_split_on,
                strip_headers=False # Keep headers in the chunk content
            )
            # split_text expects a string, so we pass doc.page_content
            doc_chunks = markdown_splitter.split_text(doc.page_content)

            # Add original document metadata to each chunk
            for chunk in doc_chunks:
                # Ensure 'source' metadata is present, useful for citations
                if 'source' not in chunk.metadata and 'source' in doc.metadata:
                    chunk.metadata['source'] = doc.metadata['source']
                # You might want to add other relevant metadata from the original doc
                # For example, the file path from ObsidianLoader
                if 'file_path' not in chunk.metadata and 'file_path' in doc.metadata:
                    chunk.metadata['file_path'] = doc.metadata['file_path']
                # If you want to include the original Obsidian file name
                if 'file_name' not in chunk.metadata:
                    chunk.metadata['file_name'] = os.path.basename(doc.metadata.get('file_path', 'unknown_file'))

            all_chunks.extend(doc_chunks)
        except Exception as e:
            print(f"Error splitting document {i} ({doc.metadata.get('file_path', 'unknown')}): {e}")

    print(f"Split documents into {len(all_chunks)} chunks.")
    if not all_chunks:
        print("No chunks generated. This might indicate an issue with the splitter or document content.")
        return

    # 3. Create Embeddings and Store in a Vector Database
    print(f"Initializing embeddings with model: {EMBEDDING_MODEL_NAME}")
    try:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    except Exception as e:
        print(f"Error initializing embedding model: {e}")
        print("Please ensure 'pip install InstructorEmbedding transformers' and the model name is correct.")
        return

    print(f"Creating and persisting vector database to: {CHROMA_DB_DIR}")
    try:
        # Chroma.from_documents directly takes a list of Document objects
        vector_db = Chroma.from_documents(
            all_chunks,
            embeddings,
            persist_directory=CHROMA_DB_DIR
        )
        vector_db.persist()
        print("Vector database created and persisted successfully!")
    except Exception as e:
        print(f"Error creating/persisting vector database: {e}")
        print("Ensure ChromaDB dependencies are met and disk space is available.")


if __name__ == "__main__":
    ingest_documents()
