from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# Use free Hugging Face embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
)

def process_content(query, web_content):
    processed_chunks = []

    for i in range(len(web_content)):
        raw_text = web_content[i]['content']
        if not raw_text:
            continue

        # Split into smaller docs
        chunks = text_splitter.create_documents([raw_text])

        # FAISS vector store
        vector_store = FAISS.from_documents(chunks, embeddings)
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

        # Retrieve top chunks
        retrieved_docs = retriever.invoke(query)
        top_texts = [doc.page_content for doc in retrieved_docs]
        web_content[i]['content'] = "\n".join(top_texts)

    return web_content
