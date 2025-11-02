import streamlit as st
from langchain.storage import LocalFileStore
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import FAISS

st.set_page_config(
    page_title="DocumentGPT",
    page_icon="1️⃣"
)

st.title("DocumentGPT")

st.markdown("""
            Welcome!
            
            Use this chatbot to ask question to an AI about your files!
""")


def embed_file(file):
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"
    st.write(file_content, file_path)
    with open(file_path, "wb") as f:
        f.write(file_content)
    cache_dir = LocalFileStore(f"./.cache/embeddings/{file.name}")
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        # seperator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)
    embeddings = OpenAIEmbeddings()
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
    vectorstore = FAISS.from_documents(docs, cached_embeddings)
    retriever = vectorstore.as_retriever()
    return retriever

file = st.file_uploader("Upload a .txt .pdf or .docx file", type=["pdf","txt","docx"])

if file:
    retriever = embed_file(file)
    retriever.invoke("who is petter")


## 아래의 코드를 더 보기 좋게 위와 같이 변경함

# file = st.file_uploader("Upload a .txt .pdf or .docx file", type=["pdf","txt","docx"])

# if file:
#     st.write(file)
#     file_content = file.read()
#     file_path = f"./.cache/files/{file.name}"
#     st.write(file_content, file_path)
#     with open(file_path, "wb") as f:
#         f.write(file_content)
#     cache_dir = LocalFileStore(f"./.cache/embeddings/{file.name}")
#     splitter = CharacterTextSplitter.from_tiktoken_encoder(
#         # seperator="\n",
#         chunk_size=600,
#         chunk_overlap=100,
#     )
#     loader = UnstructuredFileLoader(file_path)

#     docs = loader.load_and_split(text_splitter=splitter)

#     embeddings = OpenAIEmbeddings()

#     cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)

#     vectorstore = FAISS.from_documents(docs, cached_embeddings)

#     retriever = vectorstore.as_retriever()
#     docs = retriever.invoke("Who is Petter?")
#     st.write(docs)