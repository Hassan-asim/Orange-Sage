import os
import asyncio
import warnings
from typing import List
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# --- LangChain Imports ---
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# --- Load Environment Variables ---
load_dotenv()

# --- Suppress Deprecation Warnings ---
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# --- FastAPI App ---
app = FastAPI(title="Orange Sage Knowledge Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Globals ---
vectorstore = None
qa = None
DOCS_FOLDER = "temp_docs"
LOCK = asyncio.Lock()

# --- Refined SYSTEM PROMPT ---
SYSTEM_PROMPT = (
    "You are the official AI representative of **Orange Sage**, the autonomous AI-powered cybersecurity assessment platform. "
    "Your role is to educate and promote Orange Sage’s unique strengths — such as mimicking ethical hackers, dynamic vulnerability testing, "
    "controlled exploit validation, and automated security analysis — while staying professional and concise.\n\n"

    "**Rules:**\n"
    "1. **Stay On-Brand:** Always relate answers back to Orange Sage and its autonomous security capabilities.\n"
    "2. **Cybersecurity Expertise:** You may discuss security concepts (e.g., OWASP, exploits, or vulnerabilities), "
    "but must pivot to how Orange Sage helps detect, prevent, or analyse such threats.\n"
    "3. **Technical Implementation Questions:** Do *not* reveal internal code, libraries, or backend architecture. "
    "Politely decline and refocus on the product capabilities instead.\n"
    "4. **Document Context:** If an answer cannot be found in the uploaded docs (Scope, SRS, SDS, etc.), respond with "
    "**NOT_FOUND_IN_DOCS** exactly.\n"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}\n\nContext:\n{context}")
])

# --- Helper Functions ---
def build_chain_from_docs(docs):
    global vectorstore, qa

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
    )


def load_and_index_documents():
    """Load PDF/TXT documents and rebuild the RAG chain."""
    if not os.path.exists(DOCS_FOLDER):
        print(f"⚠️ Directory '{DOCS_FOLDER}' not found.")
        return

    docs = []
    print("\n📄 Starting document indexing...")
    for filename in os.listdir(DOCS_FOLDER):
        path = os.path.join(DOCS_FOLDER, filename)
        if os.path.isdir(path):
            continue

        try:
            if path.lower().endswith(".pdf"):
                loader = PyPDFLoader(path)
            elif path.lower().endswith(".txt"):
                loader = TextLoader(path, encoding="utf-8")
            else:
                continue

            docs.extend(loader.load())
            print(f"✅ Loaded: {filename}")

        except Exception as e:
            print(f"❌ Error loading {filename}: {e}")

    if docs:
        build_chain_from_docs(docs)
        print("✅ Indexing complete. Chatbot ready.")
    else:
        print("⚠️ No readable files found in temp_docs.")


@app.on_event("startup")
async def startup_event():
    """Auto-index documents on startup."""
    load_and_index_documents()


class QueryRequest(BaseModel):
    question: str


@app.post("/chat")
async def chat(request: QueryRequest):
    global qa

    if qa is None:
        raise HTTPException(status_code=400,
                            detail="RAG index not built. Upload documents or restart the server.")

    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Empty question received.")

    basic_greetings = {"hi", "hello", "hey", "how are you", "whats up"}
    if question.lower() in basic_greetings:
        return {"answer": "Hello! I'm Orange Sage's AI representative. How can I help you learn about our autonomous security platform?"}

    response = qa.invoke({"question": question})
    answer = response.get("answer") if isinstance(response, dict) else str(response)

    if "**NOT_FOUND_IN_DOCS**" in answer:
        return {"answer": "Sorry, I couldn't find relevant information in the uploaded documents."}

    return {"answer": answer}


# --- NEW: Upload Endpoint ---
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload .txt or .pdf file and trigger background re-indexing."""
    global qa

    if not file.filename.lower().endswith((".txt", ".pdf")):
        raise HTTPException(status_code=400, detail="Only .txt and .pdf files are supported.")

    os.makedirs(DOCS_FOLDER, exist_ok=True)
    file_path = os.path.join(DOCS_FOLDER, file.filename)

    async with LOCK:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        print(f"📥 Uploaded: {file.filename}")

        # Reindex asynchronously (non-blocking)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, load_and_index_documents)

    return {"message": f"✅ {file.filename} uploaded and indexed successfully!"}


@app.get("/status")
def status():
    return {"ready": qa is not None}


@app.get("/")
def root():
    return {"message": "Orange Sage Knowledge Chatbot API is running. Upload documents via /upload or chat via /chat."}
