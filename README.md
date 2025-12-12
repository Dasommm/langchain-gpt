## LangChain

:LLM(Large Language Model)을 활용한 어플리케이션을 만들기 위한 프레임워크 
https://www.langchain.com/

- https://platform.openai.com/ : openAI api 사용을 위한 사이트(결제 필요)
- https://claude.ai/ : 클로드 AI
- https://streamlit.io/ : UI 만들어주는 서비스
- https://www.pinecone.io/ : AI용 메모리 서비스
- https://huggingface.co/ :  AI용 깃헙
- https://fastapi.tiangolo.com/ : 프레임워크

---
1. ChatGPT plus 결제 : plugin store 사용을 위해 결제 필요
2. 파이썬 폴더 생성
3. git init
4. git ignore 작성
5. 파이썬 virtual env 만들기 & 해당 환경으로 들어가기:

```jsx
python -m venv ./env
source env/bin/activate
```

6. requirement.txt 붙여넣은 다음 pip install -r requirements.txt로 설치한다.
7. .env 만들어서 ai key 입력
7. git ignore에 /env와 .env 작성
7. 쥬피터 사용을 위해서 .ipynb 확장자로 파일 생성

-----
프로젝트를 실행시키기 위해서는
1. source /Users/dasom/Desktop/langchain-gpt/env/bin/activate
2. cmd + shift + P -> Python: Select Interpreter -> langchain 설치된 환경 선택
3. streamlit run Home.py