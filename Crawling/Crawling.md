## Web Crawling
두 가지 방법이 있고, 그 차이를 확인할 것.
- urllib.requests  :  bs( `html` ,'html.parser')
- requests  :  bs( `html.text` , 'html.parser')

### html 태그에서 원하는 정보 추출하기

#### find / find_all 사용해서 추출하기
```python
# class를 이용해서 원하는 정보 찾기.
find_div = soup. find('div', class_="group_nav")
# id 이용를 이용해서 원하는 정보 찾기
find_div = soup. find('div', id="NM_FAVORITE")
```
class를 이용할 때는 class 뒤에 `_`를 붙여줘야 한다. id는 붙이면 안됨.
그리고 속성값 내의 띄어쓰기에도 `_`를 넣어줘야 한다. (class, id 둘 다.)

    * `soup`은 앞서 requests와 BeautifulSoup을 통해 가져온 페이지 내용이다.

find_all로 li에 대한 리스트를 만들어 준뒤,
`find_lst = find_div.find_all('li')`

```python
for item in find_lst:
    print(item.text)  # 모든 태그를 제거하고 텍스트만 남김.
    print(item.find('a')['href'])  # 태그의 속성을 출력 - 하이퍼링크 추출
```

#### CSS Selector 사용해서 추출하기

`f12`를 누른 뒤 나타나는 창에서, 갖고오고 싶은 곳을 더블클릭 후, `마우스우클릭 - Copy - Copy Selector` 를 통해 갖고 오면 #NM_FAVORITE > div.group_nav 같이 생긴 내용이 붙여넣기 된다.

- 붙여넣어질 때 생기는 공백은 `.`으로 처리할 것.

soup.select('#NM_FAVORITE > div.group_nav')
css_soup = soup.select('#NM_FAVORITE > div.group_nav > ul.list_nav.type_fix')
