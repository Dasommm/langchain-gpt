import streamlit as st
from langchain.prompts import PromptTemplate

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