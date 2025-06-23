from extracting_todays_link import today_news_link
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings  # Local embeddings
from langchain.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader



loader = WebBaseLoader(today_news_link)
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

embedding_model = "mxbai-embed-large"  # Also try "nomic-embed-text", "mxbai-embed-large"

# 4. Create Embeddings
embeddings = OllamaEmbeddings(
    model=embedding_model,
    temperature=0.0  # For deterministic embeddings
)

# 5. Build Vector Store
vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local("ollama_vectorstore")  # Persist to disk

chunks = splitter.split_documents(docs)