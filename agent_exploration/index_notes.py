from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from fetch_notion_notes import get_all_notes_from_database
import os

db_id = "d6d2e15e842b440fa7c098a3d899fa47"
notes = get_all_notes_from_database(db_id)

docs = [Document(page_content=note) for note in notes]
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

embeddings = OpenAIEmbeddings()  # Use local embeddings if using Ollama
db = FAISS.from_documents(chunks, embeddings)
db.save_local("notion_index")
