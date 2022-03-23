# 기상청 날씨 정보 조회
## JSON 형식으로 가져오기.

```python
import requests
import json
import pandas as pd
```

```python
def urljson(시작일, 종료일, 지점코드, 행갯수 = 10):
    
    # 연결 url 작성
    인증키 = 'encoding용 인증키'
    url = "http://apis.data.go.kr/..."
    url = url + str(인증키)
    url = url + "&pageNo=1&dataCd=ASOS&dateCd=DAY&dataType=json"
    url = url + "&numOfRows=" + str(행갯수)
    url = url + "&startDt=" + str(시작일) + "&endDt=" + str(종료일)
    url = url + "&stnIds=" + str(지점코드)

    # url을 이용해 데이터 요청
    soup_json = requests.get(url)
    if soup_json.status_code != 200:
        exit('데이터를 받아오지 못함.')
    
    
    json_obj = json.loads(soup_json.content)
    
    return json_obj
```
- JSON은 BeautifulSoup과 parser가 필요 x.
- json.loads를 통해 쉽게 읽어올 수 있다
- `.content`나 `.text` 사용 사능.

```python
soup = urljson(20220101, 20220131, 294)
soup
```
결과를 확인해보면, 딕셔너리의 형태로 읽어온 것을 알 수 있다. 원하는 정보에 접근하기 위해 key를 차례로 적어서 접근한다.

```python
item = soup['response']['body']['items']['item']
```

앞서 XML로 읽어 왔을 때완 다르게, JSON형식은 바로 DataFrame으로의 변환이 가능하다.

```python
df_json = pd.DataFrame(item)
df = df_json[['stnNm', 'tm', 'avgTa', 'minTa', 'maxTa', 'sumRn', 'maxWs', 'avgWs']]
df.head()