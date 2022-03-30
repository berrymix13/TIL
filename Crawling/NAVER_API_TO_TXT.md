## 네이버 API 파일 저장

- txt 형식으로 저장

```python
from bs4 import BeautifulSoup as bs
from urllib import request
from urllib.request import quote
import urllib
import requests
import pandas as pd
import re
import os
import sys
import json
```

- 로그인 후 link 가져오는 함수

```python
# 네이버 API 로그인 후 link 정보 가져와 돌려주기
def get_Nav_client(encText, sPage):
    # 기록할 빈 파일 생성
    fq = open('c:/pydata/'+encText+'_질문.txt', "w")
    fa = open('c:/pydata/'+encText+'_답변.txt', "w")

    url = "https://openapi.naver.com/v1/search/kin?query=" + quote(encText) # json 결과
    url = url + "&start=" + str(sPage) + "&display=100"

        headers = {"X-Naver-Client-Id":'발급받은 ID', 
               "X-Naver-Client-Secret":"발급받은 PW"}

    res_content=requests.get(url, headers=headers)

    if res_content.status_code == 200:
        res_json = res_content.json()
    else:
        print("Error Code:" + str(res_json.status_code))
        sys.exit(0)
    
    fq.close()
    fa.close()
    
    df=pd.DataFrame(res_json['items'])
       
    return list(df['link'])
```

- 링크를 사용해 파일에 기록하는 함수

```python
#link를 이용해 세부 내용 가져와 파일에 기록하기
def get_write(encText, link):
    kin_html = requests.get(link)

    fq = open('c:/pydata/'+encText+'_질문.txt', "a")
    fa = open('c:/pydata/'+encText+'_답변.txt', "a")

    if kin_html.status_code != 200 :
        fq.close() # 읽지 않았다는 의미.
        fa.close() # 그냥 끝내버리면 프로그램이 끝남.
        
    else:
        kin_soup = bs(kin_html.text, "html.parser")

        # 제목 가져오기
        try:
            kin_tit = kin_soup.find("div", class_="title").get_text().replace("\n", "").replace("\t", "")
            fq.write(kin_tit+"\n")
        except:
            fq.write("\n")

        kin_body=kin_soup.find('div', class_="c-heading__content")

        # 질문 내용
        try:
            kin_body=kin_soup.find('div', class_="c-heading__content").text.replace("\n", "").replace("\t", "")
            fq.write(kin_body)
        except:
            fq.write("\n")

        # 답변 내용

        for kin_ans in kin_soup.find_all('div', class_="se-component se-text se-l-default"):
            fa.write(re.sub("[^가-힣 ]","",kin_ans.text))
        	fq.write("\n")

        fq.close()
        fa.close()
```

### 데이터 1000개를 가져와 txt로 저장

```python
#encText = urllib.parse.quote("제주도")
encText = quote("제주도")

for i in range(1, 1001,100):
    
    reg_link=get_Nav_client(encText, i)

    # link를 이용해 세부 내용 가져와 파일에 기록하기
    for link in reg_link:
        get_write(encText, link)

print("=== End ===")
```

### 데이터 1000개 가져와 DF로 저장

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
encText = urllib.parse.quote("제주도")

df_navkin=pd.DataFrame()

for i in range(1, 101,100):

    df=get_Nav_client(encText, i)
    df_navkin=pd.concat([df_navkin, df])

df_navkin
