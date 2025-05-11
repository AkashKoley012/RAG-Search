from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

print('Load embedding model...')
# Use free Hugging Face embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("Loading embedding model complete")

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
)
print("Start processing...")

def process_content(query, web_content):
    processed_chunks = []

    for i in range(len(web_content)):
    # for content in web_content:
        raw_text = web_content[i]['content']
        # url = web_content[i]['url']
        if not raw_text:
            continue
        # print(raw_text)
        # Split into smaller docs
        chunks = text_splitter.create_documents([raw_text])

        # FAISS vector store
        vector_store = FAISS.from_documents(chunks, embeddings)
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

        # Retrieve top chunks
        retrieved_docs = retriever.invoke(query)
        top_texts = [doc.page_content for doc in retrieved_docs]
        web_content[i]['content'] = "\n".join(top_texts)
        # processed_chunks.extend(top_texts) 

    # return "\n\n".join(processed_chunks)
    return web_content
