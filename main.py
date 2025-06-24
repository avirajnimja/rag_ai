from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from extacting_data import process_news_links
from extracting_todays_link import extract_news_links

news_links =extract_news_links("https://www.livemint.com/market/stock-market-news")
print(news_links)
def get_qa_chain(vectorstore, llm_model="llama3.2"):
    # Custom prompt template
    prompt_template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    Context:
    {context}
    
    Question: {question}
    
    Answer in clear, concise bullet points with proper formatting:"""
    
    custom_prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    return RetrievalQA.from_chain_type(
        llm=Ollama(model=llm_model, temperature=0.3),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(
            search_type="mmr",  # Use Max Marginal Relevance for better diversity
            search_kwargs={"k": 5}
        ),
        chain_type_kwargs={"prompt": custom_prompt},
        return_source_documents=True
    )

def query_news(qa_chain, query):
    try:
        result = qa_chain.invoke({"query": query})
        
        # Format the output better
        print("="*50)
        print(f"QUERY: {query}")
        print("="*50)
        print("\nRESPONSE:")
        print(result['result'])
        
        print("\nSOURCES:")
        for i, doc in enumerate(result['source_documents'], 1):
            print(f"{i}. {doc.metadata['source']}")
            
        return result
        
    except Exception as e:
        print(f"Error querying: {e}")
        return None
vectorstore = process_news_links(news_links)
x=get_qa_chain(vectorstore)
query_news(x,"which stock will preform good and why")