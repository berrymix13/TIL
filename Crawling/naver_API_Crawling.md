## 네이버 API를 이용한 정보 수집(크롤링)

- 네이버 개발자 센터에 가입 및 인증서 발급



```python
import os
import sys
import json
import urllib.request
import requests
```

## urllib.requests 사용

네이버 개발자 센터의 검색 기능 중 블로그에 가보면 예시 코드가 있다. 그걸 그대로 가져와 지식인에 맞게 변경했다.

```python
# 네이버 검색 API예제는 블로그를 비롯 전문자료까지 호출방법이 동일하므로 blog검색만 대표로 예제를 올렸습니다.
# 네이버 검색 Open API 예제 - 블로그 검색


client_id = "_fV4rjGKGpefS6N_jF0s"
client_secret = "I3h1sowkHN"

# 인코딩
encText = urllib.parse.quote("제주도")
#url = "https://openapi.naver.com/v1/search/kin.xml?query=" + encText # xml결과
url = "https://openapi.naver.com/v1/search/kin?query=" + encText # json 결과

# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
request = urllib.request.Request(url)
# urllib 은 데이터 못 받아오면 오류가 남
# requests는 오류는 안남. 

request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)

rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    #response_body_txt = response_body.decode('utf-8')
else:
    print("Error Code:" + rescode)
```

## requests 사용

```python
client_id = "내가 발급받은 ID"
client_secret = "내가 발급받은 PW"

encText = urllib.parse.quote("제주도")
url = "https://openapi.naver.com/v1/search/kin?query=" + encText # json 결과

#request = urllib.request.Request(url)
headers = {"X-Naver-Client-Id" :client_id,
    "X-Naver-Client-Secret":client_secret}

res_json = requests.get(url, headers = headers)

if res_json.status_code == 200:
    res_cont = res_json.json()
else:
    print("Error Code:" + str(res_json.status_code))
    sys.exit(0)
```

### 세부정보를 위한 url 요청

```python
# 데이터의 key값 확인
print(res_cont.keys())
print(res_cont['items'][0].keys())
```

```
dict_keys(['lastBuildDate', 'total', 'start', 'display', 'items'])
dict_keys(['title', 'link', 'description'])
```

```python
# 각각의 데이터 확인
# 제목
print(res_cont['items'][0]['title'])
print()
# 링크
print(res_cont['items'][0]['link'])
print()
# 내용 요약
print(res_cont['items'][0]['description'])
print()
```

#### url 정보 저장

```python
# url 정보 전체 출력
url_lst = []
for item in res_cont['items']:
    url_lst.append(item['link'])
url_lst
```

### 가져온 정보에서 제목/ 링크/ 요약을 DataFrame으로 저장

```python
import pandas as pd
df=pd.DataFrame(res_cont['items'])
df.head(2)
```

