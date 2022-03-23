<h1> 기상청 날씨 정보 조회 </h1>
- 공공데이터포털에서 [활용요청] 후 사용

```python
import requests
from bs4 import BeautifulSoup as bs
```

```python
def urlprn(시작일, 종료일, 지점코드, 행갯수 = 10):
    
    # 연결 url 작성
    인증키 = 'encoding용 인증키'
    url = "http://apis.data.go.kr/..."
    url = url + str(인증키)
    url = url + "&pageNo=1&dataCd=ASOS&dateCd=DAY&dataType=xml"
    url = url + "&numOfRows=" + str(행갯수)
    url = url + "&startDt=" + str(시작일) + "&endDt=" + str(종료일)
    url = url + "&stnIds=" + str(지점코드)

    # print(url)
    
    # url을 이용해 데이터 요청
    soup_html = requests.get(url)
    if soup_html.status_code != 200:
        exit('데이터를 받아오지 못함.')

    soup = bs(soup_html.text, 'html.parser')
    
    return soup
```


<h2> XML 형식으로 가져오기 </h2>

위의 url에서 &dataType=xml 로 설정하여 xml로 가져옴.
사용자 함수를 사용하여 url을 가져온 뒤, 필요한 데이터만 꺼내 DataFrame에 집어 넣기.
<h3> 데이터의 총 개수 파악 </h3>
    ```python
    stday = 20220101
    enday = 20220131
    pointID = 108   # Seoul

    soup = urlprn(stday, enday, pointID)
    totcnt = soup.find('totalcount').get_text()
    ```

    - Beautiful Soup으로 읽어들인 soup에는 데이터가 기본값인 10 개만 들어있기 때문에 soup의 totalcount를 사용하여 전체 데이터의 개수로 url을 다시 읽어들인다.
    - find  :   전체 중 처음 한 개만을 찾아 반환해줌
    - find_all  :  전체 내용을 찾아 '리스트'로 반환해줌.
    
     ```python
     soup = urlprn(stday, enday, pointID, totcnt)
    ```
<h3> 조회 데이터 전체를 가져와 DataFrame으로 변경하기 </h3>

    ```python
    import pandas as pd
    ```
    
    ```python
    row = [] 

    for i in range(len(items)):
        stnnm = items[i].find('stnnm').get_text()
        tm = items[i].find('tm').get_text()
        avgta = items[i].find('avgta').get_text()
        minta = items[i].find('minta').get_text()
        maxta = items[i].find('maxta').get_text()
        sumrn = items[i].find('sumrn').get_text()
        maxws = items[i].find('maxws').get_text()
        avgws = items[i].find('avgws').get_text()
    
        row.append([stnnm, tm, avgta, minta, maxta, sumrn, maxws, avgws])
        
        df1 = pd.DataFrame(row, columns=['지점명', '일자', '평균기온', '최소기온', '최대기온', '일강수량', '최대풍속', '최소풍속'])

    df1
    ```
    - JSON 형식으로 가져오면 더 편함.