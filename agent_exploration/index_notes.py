from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from fetch_notion_notes import extract_recursive
from langchain_community.embeddings import HuggingFaceEmbeddings


note_id = "d6d2e15e842b440fa7c098a3d899fa47"
notes = extract_recursive(note_id)

docs = [Document(page_content=note) for note in notes]
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"Chunks: {len(chunks)}")
print(f"First chunk (if any): {chunks[0].page_content if chunks else 'No chunks'}")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(chunks, embeddings)
db.save_local("notion_index")
