
from langchain_community.llms import Ollama  # Local LLM
from langchain.chains import RetrievalQA
from extacting_data import vectorstore
llm_model = "llama3.2"

qa_chain = RetrievalQA.from_chain_type(
    llm=Ollama(model=llm_model),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

# 7. Query the System
query = "Summarize the key news points"
result = qa_chain.invoke({"query": query})

print(f"Answer: {result['result']}")
print("\nSources:")
for doc in result['source_documents']:
    print(f"- {doc.metadata['source']}")
