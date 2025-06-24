from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup
import logging

def preprocess_document(content):
    """Clean HTML content and extract metadata"""
    soup = BeautifulSoup(content, 'html.parser')
    # Remove unwanted elements (scripts, styles, etc.)
    for element in soup(['script', 'style', 'nav', 'footer']):
        element.decompose()
    return str(soup.get_text())

def process_news_links(news_links, embedding_model="mxbai-embed-large"):
    try:
        # Load with custom processing
        loader = WebBaseLoader(news_links)
        loader.requests_kwargs = {'headers': {'User-Agent': 'Mozilla/5.0'}}
        docs = loader.load()
        
        # Add preprocessing
                
        if not docs:
            raise ValueError("No documents loaded - check URL accessibility")

        for doc in docs:
            doc.page_content = preprocess_document(doc.page_content)
        
        # Better chunking strategy
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            add_start_index=True
        )
        
        chunks = splitter.split_documents(docs)
        
        embeddings = OllamaEmbeddings(
            model=embedding_model,
            temperature=0.0
        )
        
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local("ollama_vectorstore")
        return vectorstore
        
    except Exception as e:
        logging.error(f"Error processing news links: {e}")
        raise