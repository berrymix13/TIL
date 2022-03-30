## ChromeDriver를 사용한 Crawling

<h2> 모듈 Selenium </h2>

```py
from selenium import webdriver
```

- 앞서 배운 requests를 사용해서 페이지를 크롤링 할 수 없을 때 사용
- webdriver 라는 API를 통해 운영체제에 설치된 크롬 등의 브라우저를 제어.
- 모듈 설치와 크롬 브라우저 설치가 필요하다.



```py
driver = webdriver.Chrome('c:/pydata/chromedriver.exe')

url = 'https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword=광교 맛집'
driver.get(url)
```

`driver.get(url)` 을 진행하면, 기존 크롬과 다른 창이 뜨게 된다.

<img src='![image-20220327111034319](C:\Users\sujin\AppData\Roaming\Typora\typora-user-images\image-20220327111034319.png)' />

### 웹 브라우저(HTML) 가져오기

이전까지는 `html = requests.get(url)` 을 통해 html을 불러왔다면, 이제는 `driver.page_source` 를 통해 가져올 수 있다.

```py
soup = driver.page_source
soup
```

### 원하는 태그 찾기

requests 후 BeautifulSoup을 통해 가져온 soup은 find와 find_all로 쉽게 찾을 수 있었다.
이제 크롬 드라이버를 사용한 가져오기를 실행해 보자.  

```py
txt_soup = driver.find_elements_by_css_selector('title')
txt_soup
```

그러나 이전까지의 방법으로도 태그 찾기는 가능하다. soup를 다시 BeautifulSoup으로 가져오면 된다.

```py
from bs4 import BeautifulSoup as bs 
soup = bs(html, 'html.parser')
```

requests때와는 다르게, `.text` 나 `.get_text()` 가 들어가지 않는 것을 볼 수 있다.

```py
post_soup = soup.find_all('div', class_='list_search_post')
post_soup[0]
```

`post_soup[0]`은 블로그 검색 결과 첫 번째 뜨는 블로그이 제목, 내용요약, 닉네임 등을 가져와 보여준다. 여기서 제목을 추출해보자.

#### 제목 추출

```py
title = post_soup[0].find('strong', class_='title_post').text
title
```

#### 하이퍼링크 추출

```py
herf = post_soup[0].find('a', class_='text')['herf']
print(herf)
```

### 브라우저를 이용해 페이지 제어

```python
driver.get('https://google.com')
elem = driver.find_element_by_name('q')

elem.clear() # 혹시 모를 입력되어있는 값을 지움
elem.send_keys('광교 맛집')
```

구글의 검색창에 위와 같이 검색어를 입력하면 아래 처럼 자동으로 입력되어 있는 것을 볼 수 있다.

<img src='![image-20220327114112888](C:\Users\sujin\AppData\Roaming\Typora\typora-user-images\image-20220327114112888.png)' />

- xpath 를 통해 검색 버튼을 클릭하여 검색 결과를 확인할 수 있다.

```python
driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[2]/div[2]/div[5]/center/input[1]').click()
```





