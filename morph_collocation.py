# morph_collocation.py
#-*- coding:utf-8 -*-
import urllib3
import json

morph_col_dic = {}
WINDOW_SIZE = 5

openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
accessKey = "ACCESS_KEY"
analysisCode = "morp" # 형태소 분석

# 입력 텍스트 파일을 오픈한다.
f = open("F:\\수업_2019년2학기\\05_통번역과기술\\기말고사\\busan_tour.txt", 'r', encoding='utf-8')

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

        # sentence에 포함된 morp 리스트를 반복하며 공기단어 count 계산
        length = len(s["morp"])
        for i in range(length):
            m = s["morp"][i];
            if m["type"]=="NNG" or m["type"]=="NNP" or m["type"]=="VA" or m["type"]=="VA":
                morph_key = m["lemma"] + "/" + m["type"]

                for j in range(length):
                    if i==j :
                        continue

                    if j<i-WINDOW_SIZE or j>i+WINDOW_SIZE:
                        continue
                    
                    m2 = s["morp"][j];
                    if m2["type"]=="NNG" or m2["type"]=="NNP" or m2["type"]=="VV" or m2["type"]=="VA":
                        col_key = m2["lemma"] + "/" + m2["type"]

                        merged_key = morph_key + "\t" + col_key;

                        if morph_col_dic.get(merged_key):
                            morph_col_dic[merged_key] = morph_col_dic[merged_key] + 1
                        else:
                            morph_col_dic[merged_key] = 1


# 입력 텍스트 파일 닫기
f.close()

# 전체 문장에 형태소 공기단어 빈도수를 파일에 저장하고 화면에 출력한다.
f = open("morph_collocation_count.txt", 'w', encoding='utf-8')
for k in morph_col_dic.keys():
    s = k + "\t" + str(morph_col_dic[k])
    print(s)
    f.write(s+"\n")
f.close()
