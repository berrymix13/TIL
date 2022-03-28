# 스타벅스 지역별 지점 데이터 받아오기

1. 지역별 지점 쉬치 정보 수집
     - url 가져와 데이터 수집
     - csv 로 저장

```python
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
```

## 서울 지역 매장 데이터 가져오기

홈페이지 https://www.starbucks.co.kr/store/store_map.do 에 들어가 [매장찾기] - [서울] -[전체] 버튼을 클릭해서 서울시 전체 스벅 데이터를 가져온다.

```python
browser = Chrome('c:/pydata/chromedriver.exe')

url = 'https://www.starbucks.co.kr/store/store_map.do'
browser.get(url)

### [매장찾기] 클릭
browser.find_element(By.XPATH, '//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/header[2]/h3/a').click()

### [서울] 클릭
browser.find_element(By.XPATH, 
                     '//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/article[2]/div[1]/div[2]/ul/li[1]/a').click()
time.sleep(1)

### [전체] 클릭
browser.find_element(By.XPATH, '//*[@id="mCSB_2_container"]/ul/li[1]/a').click()
```

소스코드를 받아와서 지점 리스트를 받아온다.

```python
html = browser.page_source
soup = bs(html, 'html.parser')

ul_lst = soup.find('ul', class_='quickSearchResultBoxSidoGugun')

add_soup = ul_lst.find_all('li', class_= 'quickResultLstCon')
print(len(add_soup))

stbucks = []

for add in add_soup:
    
    branch = add.find('strong').text
    lot = add.find('p').text[:-9]
    lat = add['data-lat']
    long = add['data-long']
    
    stbucks.append({'지점명' :branch, '주소' :lot, '위도' :lat, '경도' :long})


df_stb = pd.DataFrame(stbucks)
df_stb
```

이런 식으로 전국 데이터를 수집하면 되는데, 서울 버튼과 경기도 버튼을 비교해보니

```
//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/article[2]/div[1]/div[2]/ul/li[1]/a
```

```
//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/article[2]/div[1]/div[2]/ul/li[2]/a
```

li[1]과  li[2] 로 인덱싱 숫자만 달랐다. 전체 버튼이 17개였으므로,  저 부분을 유의해서 for문을 돌려주면 된다.

## 전국 매장 데이터 가져오기

다른 시/도 들과 다르게 세종시에는 [전체] 버튼이 없어 생기는 오류를 해결하기 위해 try~except 구문을 활용했다.

```python
browser = Chrome('c:/pydata/chromedriver.exe')
url = 'https://www.starbucks.co.kr/store/store_map.do'
browser.get(url)

#매장찾기
browser.find_element(By.XPATH, '//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/header[2]/h3/a').click()
df = pd.DataFrame()

for i in range(17):
    browser.find_element(By.XPATH, '//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/header[2]/h3/a').click()
    
    aa = '//*[@id="container"]/div/form/fieldset/div/section/article[1]/article/article[2]/div[1]/div[2]/ul/li['+str(i+1)+']/a'
    browser.find_element(By.XPATH, aa).click()
    time.sleep(1)
    
    try:
        browser.find_element(By.XPATH, '//*[@id="mCSB_2_container"]/ul/li[1]/a').click()
        time.sleep(1)
        
    except:
        pass
    
    html = browser.page_source
    soup = bs(html, 'html.parser')

    lst = soup.find('ul', class_='quickSearchResultBoxSidoGugun')
    add_soup = lst.find_all('li', class_= 'quickResultLstCon')

    stbucks = []
    
    for add in add_soup:
        branch = add.find('strong').text
        lot = add.find('p').text[:-9]
        lat = add['data-lat']
        long = add['data-long']
        stbucks.append({'지점명' :branch, '주소' :lot, '위도' :lat, '경도' :long})


    df1 = pd.DataFrame(stbucks)
    df = pd.concat([df,df1])

browser.clos()
df = df.reset_index(drop = True)
df
```

### 데이터 프레임 CSV로 저장하기

```python
df.to_csv('c:/pydata/starbucks_all.csv', index = False)
```

