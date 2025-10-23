import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain Imports
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate

# For embeddings + LLM
# NOTE: Suppressing the HuggingFaceEmbeddings deprecation warning to keep the code functional.
import warnings
# --- UPDATED WARNING SUPPRESSION ---
# This ensures that all future deprecation warnings from LangChain related to modules are ignored.
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
# -----------------------------------

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

app = FastAPI(title="Custom Knowledge Base Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Globals and Configuration
vectorstore = None
qa = None
DOCS_FOLDER = "temp_docs"

# --- SYSTEM PROMPT for Orange Sage Persona ---
SYSTEM_PROMPT = (
    "You are the official promotional AI agent for Orange Sage, the autonomous AI-Powered Cybersecurity Assessment Platform. "
    "Your core function is to inform and promote Orange Sage by highlighting its ability to mimic ethical hackers, "
    "dynamically execute testing code, discover vulnerabilities, and validate them through controlled exploitation. "
    "You exist to help users understand how Orange Sage eliminates manual pentesting overhead and static analysis false positives. "
    
    "**RULES:**\n"
    "1. **PROMOTION & FOCUS:** Always answer questions by relating the topic back to Orange Sage. Emphasize its features: "
    "   autonomous agents, dynamic testing, validated findings, web dashboard, and role-based access control.\n"
    "2. **CYBERSECURITY:** You may answer general cybersecurity questions (e.g., about OWASP Top 10 or common vulnerabilities), "
    "   but immediately pivot to explain how Orange Sage solves or addresses that specific problem.\n"
    "3. **CODE/TECHNICAL QUESTIONS (STRICT REFUSAL):** If the user asks highly specific, low-level technical questions about "
    "   Python libraries, code imports, framework components (like `CORSMiddleware`), or the underlying RAG/chatbot implementation "
    "   (e.g., 'What Python library are you using?', 'What is FAISS?', 'How is `CORSMiddleware` used?'), you MUST politely but firmly decline. "
    "   **Example Refusal:** 'My primary focus is the security and capabilities of the Orange Sage platform itself, not the technical build of this chat interface or its specific low-level library usage. Can I assist you with understanding our agent architecture or API contracts instead?'\n"
    "4. **CONTEXT USE:** Answer only based on the provided documents (Scope, SRS, SDS, and technical project files). If the answer (especially non-Orange Sage related) "
    "   is not present in the context, you MUST respond with the exact phrase: **NOT_FOUND_IN_DOCS**"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{question}\n\nContext:\n{context}")
    ]
)

def build_chain_from_docs(docs):
    global vectorstore, qa

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # HuggingFace embeddings
    # Note: This is the line generating the deprecation warning, but it is necessary for the current setup.
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Chain with system prompt
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
    )

def load_and_index_documents():
    """Load documents from temp_docs folder and build the RAG chain."""
    
    if not os.path.exists(DOCS_FOLDER):
        print(f"Directory '{DOCS_FOLDER}' not found. Skipping initial indexing.")
        return

    docs = []
    print(f"\n--- Starting Indexing ---")
    print(f"Loading documents from {DOCS_FOLDER}...")
    
    for filename in os.listdir(DOCS_FOLDER):
        path = os.path.join(DOCS_FOLDER, filename)
        
        # Skip directories
        if os.path.isdir(path):
             continue

        if path.lower().endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif path.lower().endswith(".txt"):
            # Ensure proper encoding for text files
            loader = TextLoader(path, encoding='utf-8')
        else:
            continue

        try:
            docs.extend(loader.load())
            print(f"Successfully loaded: {filename}")
        except Exception as e:
            # Print a clean error message and continue to the next file
            print(f"Error loading {filename}: {e}")

    if docs:
        build_chain_from_docs(docs)
        print("Indexing complete. Chatbot is ready.")
    else:
        print("No readable documents found. Chatbot is not ready.")
    print(f"--- Indexing Finished ---\n")


@app.on_event("startup")
async def startup_event():
    """Runs when the FastAPI server starts."""
    load_and_index_documents()


class QueryRequest(BaseModel):
    question: str


@app.post("/chat")
async def chat(request: QueryRequest):
    global qa
    
    # Check if RAG is ready
    if qa is None:
        raise HTTPException(status_code=400, 
                            detail="The RAG index is not built. Ensure documents are in temp_docs and the server is restarted.")

    question = request.question.strip()
    basic_greetings = ["hi", "hello", "hey", "how are you?", "whats up?"]
    if question.lower() in basic_greetings:
        return {"answer": "Hello! I am the promotional AI agent for Orange Sage. How can I help you learn about autonomous security testing?"}

    # Invoke the chain
    response = qa.invoke({"question": question})
    answer = response.get("answer") if isinstance(response, dict) else str(response)

    # --- RAG/Context Not Found Logic ---
    LLM_NOT_FOUND = "**NOT_FOUND_IN_DOCS**"
    USER_SORRY_MESSAGE = "Sorry, I couldn't find relevant information in the knowledge base documents."
    
    # Check for the LLM's special phrase (instructed via SYSTEM_PROMPT)
    if answer and LLM_NOT_FOUND in answer:
        return {"answer": USER_SORRY_MESSAGE}
    
    return {"answer": answer}


@app.get("/status")
def status():
    return {"ready": qa is not None}


@app.get("/")
def root():
    return {"message": "Custom Knowledge Base Chatbot API. Indexing runs automatically on startup."}
