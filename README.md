## LangChain

:LLM(Large Language Model)을 활용한 어플리케이션을 만들기 위한 프레임워크 
https://www.langchain.com/

- https://platform.openai.com/ : openAI api 사용을 위한 사이트(결제 필요)
- https://claude.ai/ : 클로드 AI
- https://streamlit.io/ : UI 만들어주는 서비스
- https://www.pinecone.io/ : AI용 메모리 서비스
- https://huggingface.co/ :  AI용 깃헙
- https://fastapi.tiangolo.com/ : 프레임워크
- https://ollama.com/ : open model을 로컬에서 사용할 수 있도록 하는 서비스 -> 로컬 다운로드 필요
- https://docs.ollama.com/ : ollama docs
- https://platform.openai.com/docs/models : openAI model list
- https://platform.openai.com/tokenizer : tokenizer
- https://docs.langchain.com/: python langchain docs
- https://docs.langchain.com/oss/python/integrations/tools: langchain에서 사용할 수 있는 toolkit list

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

-----
SSL 오류 발생시(mac에서)
1. spotlight에서 "install certificates.command를 찾은 후, 더블클릭으로 실행시켜준다.
또는
1. command 창에서 
/Applications/Python\ 3.x/Install\ Certificates.command
을 실행한다. 


-------
1. brew install cloudflared
2. fast api로 코드 작성
3. uvicorn main:app --reload  ::: main 파일을 실행함
4. fast api로 작성한 함수를 url로 호출하면 내용을 브라우저에서 확인 할 수 있다
ex. http://127.0.0.1:8000/quote : 리턴 값이 json 형태로 브라우저에서 보여짐
    http://127.0.0.1:8000/docs : swagger처럼 문서가 브라우저에서 보여짐
    http://127.0.0.1:8000/openapi.json : api 설명을 위한 표준 schema를 볼 수 있음
5. localhost 서버를 배포하기 위해서 cloudflared 실행 : url 요청이 들어오면 나의 로컬호스트로 요청을 리다이렉트 해달라는 의미 
    cloudflared tunnel --url http://127.0.0.1:8000
6. 실행이 되면 url을 제공해준다. : https://basically-experience-precipitation-dubai.trycloudflare.com/