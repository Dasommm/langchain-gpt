import streamlit as st

st.set_page_config(
    page_title="GPT Practice",
    page_icon="✏️"
)

## pages에 파일을 만들면 자동으로 사이드바에 나타나게 되고, 생성한 파일명으로 보여진다.
## 정렬을 하고 싶다면 파일명 앞에 숫자로 정렬을 해준다 (ex. 01_DocumentGPT...) 앞에 작성한 숫자는 페이지에서 보여지지 않는다.

st.markdown(
    """
    # Hello!

    Welcome to my GPT Portfoloi!

    Here are the apps I made:

    - [ ] [DocumentGPT](/DocumentGPT)
    - [ ] [PrivateGPT](/PrivateGPT)
    - [ ] [QuizGPT](/QuizGPT)
    - [ ] [SiteGPT](/SiteGPT)
    - [ ] [MeetingGPT](/MeetingGPT)
    - [ ] [InvestorGPT](/InvestorGPT)
"""
)
