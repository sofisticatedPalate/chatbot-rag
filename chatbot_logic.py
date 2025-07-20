from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.llms import HuggingFacePipeline # For local models
# from langchain_openai import ChatOpenAI # For OpenAI models
from langchain_google_genai import ChatGoogleGenerativeAI # For Google models
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# Create a retriever
retriever = vector_db.as_retriever(search_kwargs={"k": 5}) # Retrieve top 5 relevant chunks

# For a local model (requires transformers and a model downloaded/accessible)
# from transformers import pipeline
# llm = HuggingFacePipeline(pipeline=pipeline("text-generation", model="distilgpt2", trust_remote_code=True))

# For OpenAI (replace with your API key)
# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# For Google (replace with your API key)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite", temperature=0)

# Define a prompt template for the LLM
prompt_template = """Use the following pieces of context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
----------------
{context}

Question: {question}
"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)

# Create the RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm, # Your chosen LLM from Step 6
    chain_type="stuff", # Puts all retrieved documents into the prompt
    retriever=retriever, # Your retriever from Step 5
    return_source_documents=True, # Optional: to show which documents were used
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)
