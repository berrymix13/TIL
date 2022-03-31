### 파일 경로 리스트를 이용해 파일 읽어오기

```python
from glob import glob

dir_path = 'C:/pydata/seoul_bicycle/'
file_lst = glob(dir_path + '*자전거*.csv')
print(file_lst)
```

> ['C:/pydata/seoul_bicycle\\서울특별시 공공자전거 이용정보(시간대별)_21.01.csv', 'C:/pydata/seoul_bicycle\\서울특별시 공공자전거 이용정보(시간대별)_21.02.csv', 'C:/pydata/seoul_bicycle\\서울특별시 공공자전거 이용정보(시간대별)_21.03.csv', 'C:/pydata/seoul_bicycle\\서울특별시 공공자전거 이용정보(시간대별)_21.04.csv', 'C:/pydata/seoul_bicycle\\서울특별시 공공자전거 이용정보(시간대별)_21.05.csv', 'C:/pydata/seoul_bicycle\\서울특별시 공공자전거 이용정보(시간대별)_21.06.csv', 'C:/pydata/seoul_bicycle\\서울특별시 공공자전거 이용정보(시간대별)_21.07.csv', 'C:/pydata/seoul_bicycle\\서울특별시 공공자전거 이용정보(시간대별)_21.08.csv', 'C:/pydata/seoul_bicycle\\서울특별시 공공자전거 이용정보(시간대별)_21.09.csv', 'C:/pydata/seoul_bicycle\\서울특별시 공공자전거 이용정보(시간대별)_21.10.csv', 'C:/pydata/seoul_bicycle\\서울특별시 공공자전거 이용정보(시간대별)_21.11.csv', 'C:/pydata/seoul_bicycle\\서울특별시 공공자전거 이용정보(시간대별)_21.12.csv']

- `*자전거*.csv`  :  파일 명에 자건거가 표함되어 있고 csv로 끝나는 파일만을 glob를 사용해 갖고올 것. 
- `glob`  :  폴더 내 파일들의 파일경로를  **리스트 ** 형태로 반환함.



### 파일 병합하기

```python
seoul_bike_m=pd.merge(seoul_bike, dfs_group, on="대여소번호")  
display(seoul_bike_m)
```

- on 을 기준으로 파일이 합쳐진다.
- how   :  생략=>공동, "outer"=>전체, 'left' =>왼쪽기준, 'right'=>오른쪽 기준