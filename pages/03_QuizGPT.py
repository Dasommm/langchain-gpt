## 내가 제공한 파일에 대해서 사용자에게 퀴즈를 제공한다.

import streamlit as st
import json
from langchain.retrievers import WikipediaRetriever
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.schema import BaseOutputParser

class JsonOutputParser(BaseOutputParser):
    def parse(self, text):
        text = text.replace("```", "").replace("json","")
        return json.loads(text)
    
output_parser = JsonOutputParser()


st.set_page_config(page_title="QuizGPT", page_icon="❓")

st.title("QuizGPT")

llm = ChatOpenAI(
    temperature=1,
    model="gpt-5-2025-08-07",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
)


def format_docs(docs):
    return "\n\n".join(document.page_content for document in docs)


questions_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
        You are a helpful assistant that is role playing as a teacher.

        Based ONLY on the following context make 10 questions to test the user's knowledge about the text.

        Each question should have 4 answers, three of them must be incorrect and one should be correct.

        Use (o) to signal the correct answer.

        Question examples:

        Question: What is the color of the ocean?
        Answers: Red|Yellow|Green|Blue(o)

        Question: What is the capital or Georgia?
        Answers: Baku|Tbilisi(o)|Manila|Beirut

        Question: When was Avatar released?
        Answers: 2007|2001|2009(o)|1998

        Question: Who was Julius Caesar?
        Answers: A Roman Emperor(o)|Painter|Actor|Model

        Your turn!

        Context: {context}
        """,
        )
    ]
)

questions_chain = {"context": format_docs} | questions_prompt | llm


formatting_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a powerful formatting algorithm.

            You format exam questions into JSON format.
            Answers with (o) are the correct ones.

            Example Input:
            Question: What is the color of the ocean?
            Answers: Red|Yellow|Green|Blue(o)

            Question: What is the capital or Georgia?
            Answers: Baku|Tbilisi(o)|Manila|Beirut

            Question: When was Avatar released?
            Answers: 2007|2001|2009(o)|1998

            Question: Who was Julius Caesar?
            Answers: A Roman Emperor(o)|Painter|Actor|Model


            Example Output:

            ```json
            {{ "questions": [
                {{
                "question": "What is the color of the ocean?",
                "answers": [
                    {{
                    "answer": "Red",
                    "correct": false
                    }},
                    {{
                    "answer": "Yellow",
                    "correct": false
                    }},
                    {{
                    "answer": "Green",
                    "correct": false
                    }},
                    {{
                    "answer": "Blue",
                    "correct": true
                    }},
                ]
                }},
                {{
                "question": "What is the capital or Georgia?",
                "answers": [
                    {{
                    "answer": "Baku",
                    "correct": false
                    }},
                    {{
                    "answer": "Tbilisi",
                    "correct": true
                    }},
                    {{
                    "answer": "Manila",
                    "correct": false
                    }},
                    {{
                    "answer": "Beirut",
                    "correct": false
                    }},
                ]
                }},
                {{
                "question": "When was Avatar released?",
                "answers": [
                    {{
                    "answer": "2007",
                    "correct": false
                    }},
                    {{
                    "answer": "2001",
                    "correct": false
                    }},
                    {{
                    "answer": "2009",
                    "correct": true
                    }},
                    {{
                    "answer": "1998",
                    "correct": false
                    }},
                ]
                }},
                {{
                "question": "Who was Julius Caesar?",
                "answers": [
                    {{
                    "answer": "A Roman Emperor",
                    "correct": true
                    }},
                    {{
                    "answer": "Painter",
                    "correct": false
                    }},
                    {{
                    "answer": "Actor",
                    "correct": false
                    }},
                    {{
                    "answer": "Model",
                    "correct": false
                    }},
                ]
                }}
            ]
            }}
            ```
            Your turn!
            Questions: {context}
            """,
        )
    ]
)

formatting_chain = formatting_prompt | llm


@st.cache_data(show_spinner="Loading file....")
def split_file(file):
    file_content = file.read()
    file_path = f"./.cache/quiz_files/{file.name}"
    # st.write(file_content, file_path)
    with open(file_path, "wb") as f:
        f.write(file_content)
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        # seperator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )
    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)
    return docs

@st.cache_data(show_spinner="Making Quiz...")
def run_quiz_chain(_docs, topic):
    chain = {"context": questions_chain} | formatting_chain | output_parser
    return chain.invoke(_docs)

@st.cache_data(show_spinner="Searchig Wikipedia...")
def wiki_search(term):
    retriver = WikipediaRetriever(top_k_results=3)  ## top_k_results는 맨 위에서 해당 갯수만큽 결과값을 가져온다는 옵션
    return retriver.get_relevant_documents(term)


with st.sidebar:
    docs = None
    choice = st.selectbox("Choose what you want to use.", ("File", "Wikipidia Article"))
    if choice == "File":
        file = st.file_uploader(
            "Upload a .docx, .txt or .pdf file", type=["pdf", "txt", "docx"]
        )
        if file:
            docs = split_file(file)
    else:
        topic = st.text_input("Search Wikipedia...")
        if topic:
            docs = wiki_search(topic)

if not docs:
    st.markdown(
        """
    Welcome to QuizGPT.
                
    I Will make a quiz from Wikipedia articles or files you upload to test your knowledge and help you study.
    Get started by uploading a file or searching on Wikipedia in the sidebar.
        """
    )
else:
    # st.write(docs)
    # start = st.button("Generate Quiz")
    # if start:
    #     # question_response = questions_chain.invoke(docs)
    #     # st.write(question_response.content)
    #     # formatting_response = formatting_chain.invoke({
    #     #     "context": question_response.content
    #     # })
    #     # st.write(formatting_response.content)
    #     response = run_quiz_chain(docs, topic if topic else file.name)
    #     st.write(response)
        
        
        ## 이제 캐시가 되기 때문에 위의 버튼이 필요없음.
        ## 버튼을 없앤다
        response = run_quiz_chain(docs, topic if topic else file.name)
        # st.write(response)
    
        with st.form("questions_form"):
            # st.write(response)
            for question in response["questions"]:
                st.write(question["question"])
                value = st.radio(
                    "Select an option.",
                    [answer["answer"] for answer in question["answers"]],
                    index=None,
                )
                st.write(value)
                if {"answer": value, "correct": True} in question["answers"]:
                    st.success("Correct!")
                elif value is not None:
                    st.error("Wrong!")
            button = st.form_submit_button()
    