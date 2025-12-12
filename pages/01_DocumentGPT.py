import streamlit as st
from langchain.storage import LocalFileStore
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler

## 파일을 업로드한 후 해당 파일의 내용에 대한 정보를 알려주는 페이지

st.set_page_config(
    page_title="DocumentGPT",
    page_icon="1️⃣"
)

st.title("DocumentGPT")

st.markdown("""
            Welcome!
            
            Use this chatbot to ask question to an AI about your files!

            Upload your files on the sidebar.
""")

# event들을 listen하는 여러 function들을 가진다.
class ChatCallbackHandler(BaseCallbackHandler):
    message = ""

    def on_llm_start(self, *args, **kwargs):
        # with st.sidebar:
        #     st.write("llm started!")
        self.message_box = st.empty()
    
    def on_llm_end(self, *args, **kwargs):
        save_message(self.message, "ai")
        # with st.sidebar:
        #     st.write("llm ended!")
    
    def on_llm_new_token(self, token, *args, **kwargs):
        # print(token)
        self.message += token
        self.message_box.markdown(self.message)

llm = ChatOpenAI(
    temperature= 0.1,
    streaming=True,
    callbacks=[
        ChatCallbackHandler(),
    ]
)


@st.cache_data(show_spinner="Embedding file....")
def embed_file(file):
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"
    # st.write(file_content, file_path)
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


def save_message(message, role):
    st.session_state["messages"].append({"message":message, "role":role})

def send_message(message,role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        save_message(message, role)


def paint_history():
    for message in st.session_state["messages"]:
        send_message(message["message"], message["role"],save=False)

def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
    Answer the question using ONLY the following context. If you don't know the answer, just say you don't know. DON'T make anything up.
     Context: {context}
    """),
    ("human", "{question}")
])


with st.sidebar:
    file = st.file_uploader("Upload a .txt .pdf or .docx file", type=["pdf","txt","docx"])

if file:
    retriever = embed_file(file)
    send_message("I'm ready! Ask anything!", 'ai', save=False)
    paint_history()
    message = st.chat_input("Ask anything about your file...")
    # st.write("🌴".join(["a","b","c"]))  ## seperator
    if message:
        # -------- 이렇게 돌아가는 내용을 ----
        # send_message(message, "human")
        # docs = retriever.invoke(message)
        # docs = "\n\n".join(document.page_content for document in docs)
        # prompt = template.format_messages(context=docs, question=message)
        # # st.write(prompt)
        # llm.predict_messages(prompt)
        # ---------아래와 같이 간단하게 작성한다
        send_message(message, "human")
        chain = {
            "context": retriever | RunnableLambda(format_docs) ,
            "question": RunnablePassthrough()
        } | prompt | llm
        with st.chat_message("ai"):
            chain.invoke(message)
        # send_message(response.content, "ai")
        


else:
    st.session_state["messages"] = []




## ========================================================================================= ##
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