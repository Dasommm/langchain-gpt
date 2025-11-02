# test.py
## NLTK(Natural Language Toolkit) 라이브러리에서 'punkt' 토크나이저 데이터가 없어서 발생하는 문제 해결 스크립트

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')