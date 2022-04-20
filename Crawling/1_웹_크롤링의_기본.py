#!/usr/bin/env python
# coding: utf-8

# ## 웹 크롤링
# - 교재 직장인을 위한 데이터분석 참고 (but, 셀리늄만 나와서 아쉽)
# - 일반적인 방법은 reqest, 불가한 경우 셀리늄
# 
# - 웹 크롤러는 웹 문서, 이미지 등을 주기적으로 수집하여 자동으로 데이터베이스화하는 프로그램
# - 크롤러가 하는 작업을 의미(Web Crawling)
# - requests와 BeautifulSoup4
# - url lib reuests는 구버전이지만, 사용하게 될 경우도 있음.

# ### 1. 웹 문서 전체 가져오기
# - urllib,requests  :  bs( `html` ,'html.parser')
# - requests  :  bs( `html.text` , 'html.parser')

# In[ ]:


from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup as bs


# In[ ]:


# urlopen
html = urlopen('http://www.naver.com/')
soup = bs(html, 'html.parser')
print(soup)


# In[ ]:


# requests 
html = requests.get('http://www.naver.com/')

soup = bs(html.text, 'html.parser')
print(soup)


# ### 2. html 태그에서 원하는 정보 추출하기
# - html 태그 이용  :  find / find_all
#     * find('태그')  -  첫 번때 태그만 검색
#     * find_all('태그')  -  태그 전체를 검색해 리스트 형태로 반환
#     
# - CSS Sellector 이용
# - javascript
# 

# #### find / find_all 사용

# - 굳이 현재 있는 데이터에서 class찾아보기
# - 'div' 따로, 'class_'에는 언더바 필요! id에는 불필요!
#     `soup.find('div', class_="momo")`

# In[ ]:


# class 이용
find_div = soup. find('div', class_="group_nav")
# id 이용
find_div = soup. find('div', id="NM_FAVORITE")


# In[ ]:


# find_all 사용
find_div = soup. find('div', class_="group_nav")

# soup 대신 위에서 찾은 find_div에서 찾기
find_lst = find_div.find_all('li')
print(len(find_lst))
#print(find_lst)
for item in find_lst:
    print(item.text)  # 모든 태그를 제거하고 텍스트만 남김.
    print(item.find('a')['href'])  # 태그의 속성을 출력 - 하이퍼링크 추출


# #### Selector 사용

# In[ ]:


# copy - Copy selletor

# `#`이 들어 있으면 id, > 이후가 div.
soup.select('#NM_FAVORITE > div.group_nav')

# 클래스 네임에 들어있는 공백은 . 으로 대체함.

css_soup = soup.select('#NM_FAVORITE > div.group_nav > ul.list_nav.type_fix')

# 맨 뒤에 (1)이 붙어있음 -> for문으로 갖고와야 됨.
#NM_FAVORITE > div.group_nav > ul.list_nav.type_fix > li:nth-child(1)


# In[ ]:


# 클래스 네임에 들어있는 공백은 . 으로 대체함.

css_soup = soup.select('#NM_FAVORITE > div.group_nav > ul.list_nav.type_fix')


# ### [크롤링 연습]
# - 네이버 지식인에서 '선릉역'검색 후 검색결과 가져오기

# In[ ]:


import requests
from bs4 import BeautifulSoup as bs

url = 'https://kin.naver.com/search/list.naver?query=%EC%84%A0%EB%A6%89%EC%97%AD'

# url에서 데이터 요청
html = requests.get(url)

# 우리가 활용할 수 있도록 요청 데이터 파싱 진행
soup = bs(html.text, 'html.parser')

# css를 이용한 태그 검색
ul_soup = soup.select('#s_content > div.section > ul')

# 검색한 태그에서 li 전체를 다시 검색
li_soup = ul_soup[0].find_all('li') #[0]을 꼭 붙일 것! 리스트라서~

### 검색한 li_soup (태그) 에서 크롤링(추출) 작업 ###
# 제목
print(li_soup[0].find('dt').text )

# 게시 날짜
print(li_soup[0].find('dd').text )

# 내용
# dd인데, 몇 번째 dd인가?
# 편하게 찾긴 했지만, 또다시 리스트로 나와서 아래의 작업을 해줘야 됨.
print(li_soup[0].select('dl > dd:nth-child(3)'))
print()
print(li_soup[0].select('dl > dd:nth-child(3)')[0])
print()
print(li_soup[0].select('dl > dd:nth-child(3)')[0].text)


# #### [미션] 1페이지 검색 결과에서 전체 내용 가져오기
# - 제목, 등록일, 요악 부분을 각각 가져와 DataFrame 으로 저장하기

# In[ ]:


print(li_soup[1].find('dt').text )


# In[ ]:


len(li_soup)


# In[ ]:


nav_kin = []
for li in li_soup:
    title = li.find('dt').text.replace('\n','')
    date = li.find_all('dd')[0].text
    doct = li.find_all('dd')[1].text
    
    nav_kin.append({'제목':title, '등록일':date, '요약':doct})
print(nav_kin)


# In[ ]:


import pandas as pd
df = pd.DataFrame(nav_kin)
df #비정형 데이터 


# ### 3. 검색어를 이용한 크롤링
# - urlib 패키지의 parse 모듈 이용

# In[ ]:


from urllib import parse

text = '선릉역' #검색어

#컴퓨터 언어로 인코딩 
enc = parse.quote(text) 
print(enc) 

# 컴퓨터 언어를 사람이 알아볼 수 있는 상태로 디코딩
dec = parse.unquote('%EC%84%A0%EB%A6%89%EC%97%AD')
dec


# ### 4. 검색된 내용 전체(페이지 이동)

# In[ ]:


import requests
from bs4 import BeautifulSoup as bs
from urllib import parse
import pandas as pd

# 검색어 입력받기
text = input('검색어를 입력하세요 :')
nav_kin = []
for page in range(1,11):
    url = 'https://kin.naver.com/search/list.naver?query='+ parse.quote(text) 
    url += '&page=' + str(page)

    # url에서 데이터 요청
    html = requests.get(url)

    # 우리가 활용할 수 있도록 요청 데이터 파싱 진행
    soup = bs(html.text, 'html.parser')

    # css를 이용한 태그 검색
    ul_soup = soup.select('#s_content > div.section > ul')

    # 검색한 태그에서 li 전체를 다시 검색
    li_soup = ul_soup[0].find_all('li') #[0]을 꼭 붙일 것! 리스트라서~

    ### 검색한 li_soup (태그) 에서 크롤링(추출) 작업 ###
    for li in li_soup:
        title = li.find('dt').text.replace('\n','')
        date = li.find_all('dd')[0].text
        doct = li.find_all('dd')[1].text

        nav_kin.append({'제목':title, '등록일':date, '요약':doct})

df = pd.DataFrame(nav_kin)
df


# In[ ]:





# In[ ]:




