# ne_sentiment.py
#-*- coding:utf-8 -*-
import urllib3
import json

ne_va_dic = {}
stopword_dic = {"있/VA":1, "같/VA":1}

openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
accessKey = "ACCESS_KEY"
analysisCode = "ner" # 형태소 분석 + 개체명 인식

# 입력 텍스트 파일을 오픈한다.
f = open("busan_tour.txt", 'r', encoding='utf-8')

# 텍스트파일에서 1라인씩 읽어서 언어분석 후, 형태소의 빈도수를 누적 count한다.
while True:
    # file에서 1개 라인을 읽는다.
    line = f.readline()
    if not line: break

    # 읽은 line 1개를 API 입력 형식으로 변환
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

    # sentence 리스트에서 sentence 1개씩 순차적으로 처리하기
    for s in result_json["return_object"]["sentence"]:

        # sentence에 포함된 NE 리스트를 반복하며 공기하는 형용사 빈도수 계산
        for ne in s["NE"]:
            if ne["type"].startswith("PS") or ne["type"].startswith("LC") or ne["type"].startswith("OG") :
                ne_key = ne["text"] + "/" + ne["type"]


                # 1개의 개체명에 대해서, 해당 문장에 나타나는 형용사(va)를 추출
                for m2 in s["morp"]:
                    if m2["type"]=="VA":
                        va_key = m2["lemma"] + "/" + m2["type"]

                        # 형용사가 sotpword 중 1개이면 count하지 않음 
                        if stopword_dic.get(va_key):
                            continue;

                        # 개체명과 형용사 연결을 key로 하고 빈도수를 value로 하여 dictionary에 추가
                        merged_key = ne_key + "\t" + va_key;

                        if ne_va_dic.get(merged_key):
                            ne_va_dic[merged_key] = ne_va_dic[merged_key] + 1
                        else:
                            ne_va_dic[merged_key] = 1



# 입력 텍스트 파일 닫기
f.close()

# 전체 문장에 형태소 빈도수를 파일에 저장하고 화면에 출력한다.
f = open("ne_count.txt", 'w', encoding='utf-8')
for k in ne_va_dic.keys():
    s = k + "\t" + str(ne_va_dic[k])
    print(s)
    f.write(s+"\n")
f.close()
