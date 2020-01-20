# ne_count.py
#-*- coding:utf-8 -*-
import urllib3
import json

ne_dic = {}

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

        # sentence에 포함된 NE 리스트를 반복하며 count 계산
        for ne in s["NE"]:
            if ne["type"].startswith("PS") or ne["type"].startswith("LC") or ne["type"].startswith("OG") :
                ne_key = ne["text"] + "/" + ne["type"]
                if ne_dic.get(ne_key):
                    ne_dic[ne_key] = ne_dic[ne_key] + 1
                else:
                    ne_dic[ne_key] = 1



# 입력 텍스트 파일 닫기
f.close()

# 전체 문장에 형태소 빈도수를 파일에 저장하고 화면에 출력한다.
f = open("ne_count.txt", 'w', encoding='utf-8')
for k in ne_dic.keys():
    s = k + "\t" + str(ne_dic[k])
    print(s)
    f.write(s+"\n")
f.close()
