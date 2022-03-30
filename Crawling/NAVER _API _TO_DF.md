# NAVER API DF 저장

```python
from bs4 import BeautifulSoup as bs
import urllib
import requests
import pandas as pd
import re
import os
import sys
import json
```

```python
# 네이버 API 로그인 후 link 정보 가져와 돌려주기
def get_Nav_client(encText, sPage):
	
    # url 생성
    url = "https://openapi.naver.com/v1/search/kin?query=" + encText # json 결과
    url = url + "&start=" + str(sPage) + "&display=100"

    headers = {"X-Naver-Client-Id":"발급받은 ID", 
               "X-Naver-Client-Secret":"발급받은 PW"}
	
    # NAVER API Login
    res_content=requests.get(url, headers=headers) 

    if res_content.status_code == 200:
        res_json = res_content.json() # 200이면 데이터 갖고 옴.
    else:
        print("Error Code:" + str(res_json.status_code))
        sys.exit(0) # 못 갖고 오면 종료.

    df = pd.DataFrame(res_json['items']) # df 생성
    
    df_body = get_write(list(df['link'])) # 링크만 추출해 list 생성
    
    df=pd.concat([df, df_body], axis=1)
    #display(df.head(3))   
    return df
```

```python
# 위에서 받은 link_lst를 이용해 세부 내용 가져와 파일에 기록하기
def get_write(reg_link):
    body_lst = []
    for link in reg_link:
        kin_html = requests.get(link)

        if kin_html.status_code != 200 :
            print("Error Code:" + str(res_json.status_code))
            body_lst.append({"질문":"질문없음", "답변":"답변없음"})
		else:
            kin_soup = bs(kin_html.text, "html.parser")

            # 질문 내용
            try:
                kin_body=kin_soup.find('div', class_="c-heading__content").text.replace("\n", "").replace("\t", "")
            except:
                kin_body="질문없음"

            # 답변 내용
            ans = ""
            try:
                for kin_ans in kin_soup.find_all('div', class_="se-component se-text se-l-default"):
                    txt=re.sub("[^가-힣 ]","",kin_ans.text)
                    ans = ans + txt +"\n"
            except:
                ans="답변없음"

            body_lst.append({"질문":kin_body, "답변":ans})
    df_body=pd.DataFrame(body_lst)
    #display(df_body.head(3))
    return df_body
```

```python
encText = urllib.parse.quote("제주도")

# 최종 데이터 저장용 DF
df_navkin=pd.DataFrame()

for i in range(1, 101,100):

    df=get_Nav_client(encText, i)
    df_navkin=pd.concat([df_navkin, df])

df_navkin
```

```python
df_navkin.to_csv('c:/pydata/'+encText+'_지식인.csv')
```

