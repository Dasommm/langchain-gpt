import streamlit as st
from langchain.prompts import PromptTemplate
import time

st.title("Hello world!")

st.subheader("Welcome to Streamlit")

st.markdown(
    """
### I love it
    """
)

st.write("hello")

st.write([1,2,3,4])

st.write({"x":1})

st.write(PromptTemplate) ## 클래스를 가져올 수도 있음

p = PromptTemplate.from_template("xxxx")
st.write(p)

# 위와 같은 여러 방식으로 streamlit을 사용할 수 있다.
# 만약에 변수만 적어도 화면에 print 되어진다.
p

# 사용할 수 있는 api : https://docs.streamlit.io/develop/api-reference
st.selectbox("Choose your model",("GPT3","GPT4"))


## 데이터가 변경(셀렉트박스에서 값을 선택했다던지..)이 될때마다 전체 파일이 재실행된다.
## 새로운 부분만 refresh되는 것과 달리 전체가 재실행된다.

value = st.slider("temperture",min_value=0.1, max_value=1.0)


## sidebar 패턴
with st.sidebar:
    st.title("sidebar title")
    st.text_input("xxx")

## tab 패턴
tab_one, tab_two, tab_three = st.tabs(["A","B","C"])

with tab_one:
    st.write("a")
with tab_two:
    st.write("b")
with tab_three:
    st.write("c")



## streamlit이 가진 chat element 사용하기 : 
# chat_message() - human, ai, asistant, user 등 입력할 수 있다.
# chat_input(), chat_status()

with st.chat_message("human"):
    st.write("Hello")


with st.chat_message("ai"):
    st.write("How are you")

with st.status("Embedding file...", expanded= True) as status:
    time.sleep(2)
    st.write("Getting the file")
    time.sleep(2)
    st.write("Embedding the tile")
    time.sleep(2)
    st.write("Caching the file")
    status.update(label="Error", state="error") ## 어떻게 보여줄 것인지 

st.chat_input("Send a message to a AI")