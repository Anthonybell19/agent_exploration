from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.llms import Ollama

# Load vector store
db = FAISS.load_local("notion_index", OpenAIEmbeddings())
retriever = db.as_retriever()

llm = Ollama(model="mistral")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

while True:
    query = input("Ask a question about your notes: ")
    if query.lower() in ["exit", "quit"]:
        break
    answer = qa_chain.run(query)
    print("Answer:", answer)
