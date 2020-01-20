# morph_count_wordcloud.py
#-*- coding:utf-8 -*-
import urllib3
import json

# wordcloud를 위한 라이브러리
# 설치: pip install wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# 한글폰트/글꼴 적용
# 네이버 나눔글꼴 : https://hangeul.naver.com/2017/nanum
hangul_font_path = 'c:\\windows\\fonts\\NanumGothic.ttf'
wordcloud = WordCloud(
    font_path = hangul_font_path,
    width = 800,
    height = 800
)

# ETRI open API 정보
openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
accessKey = "38c0d4c2-a98e-4a86-8978-5aa08dba31a7"
analysisCode = "dparse"


# 텍스트 파일을 오픈한다.
# 문장 단위로 형태소 분석하여 일반명사, 고유명사, 동사, 형용사만 추출하여 wctext에 저장
f = open("F:\\수업_2019년2학기\\05_통번역과기술\\sampletext.txt", 'r', encoding='utf-8')

wctext_morp = ""

while True:
    line = f.readline() # 텍스트파일에서 1문장 읽음.
    if not line: break

    # 읽은 line 1개를 API 입력으로 할당
    requestJson = {
        "access_key": accessKey,
        "argument": {
            "text": line.strip(), # 파일에서 읽은 1문장
            "analysis_code": analysisCode
        }
    }

    # API에 전송하여 분석된 결과를 받아옴
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
     
    # 분석결과 (JSON 형식)에서 형태소 정보 추출하기
    result_str = str(response.data,"utf-8")
    result_json = json.loads(result_str)

    # sentence 배열에서 sentence 1개씩 순차적으로 처리하기
    for s in result_json["return_object"]["sentence"]:


        # read morph result (형태소정보)
        for m in s["morp"]:
            # 일반명사, 고유명사, 동사, 형용사만 저장. 나머지는 버림
            if m["type"]=="NNG" or m["type"]=="NNP" or m["type"]=="VV" or m["type"]=="VA" :
                wctext_morp = wctext_morp + " " + m["lemma"]

        
# 입력 텍스트 파일 닫기
f.close()

# wordcloud 그리기
wordcloud = wordcloud.generate(wctext_morp)

fig = plt.figure(figsize=(12,12))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
