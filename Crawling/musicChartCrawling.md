# 벅스 뮤직 크롤링 후 아티스트 분석 및 시각화
- `matplotlib` 사용 시 한글이 깨지는 문제를 해결하기 위해, 폰트를 다운받는다. 
```python
!sudo apt-get install -y fonts-namu
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf
```
- 실행 후 반드시 '런타임 다시 시작'을 실행해줄것!

### 시작일과 종료일을 입력받고 그 사이의 날짜를 전부 생성하기
```py
start_date = 20220201
end_date = 20220323
date = pd.date_range(start_date, end_date) # 사이에 있는 모든 날짜가 1일 단위로 리스트 반환 됨.
```
`2022-02-01 00:00:00`의 형식으로 생성되므로,  url에 넣기 알맞는 형태로 변경해준다.
`.strftime('%Y%m%d')` 를 붙여주면 `20220201`이 된다.

### 날마다 받아온 데이터 연결하기.
for문을 이용해서 순차적으로 받아오면 되고, 각 데이터를 list에 널은 뒤 pd를 이용한 DataFrame에 넣어주면 됨. 각각의 DF를 이어줄 때는 pd.concat([df1,df2])를 사용하며, 행 인덱스의 중복이 생기기 때문에 `df.reset_index(drop = True)`를 실행해준다.


## 꺽은선 그래프로 시각화 진행하기.
꺽은선 그래프의 x축은 날짜, Y축은 데이터를 받아올 때 만들어준 점수를 이용한다.
- 점수 : 1등 = 100점, 100등 = 1점
 앞서 설치한 글꼴을 이제 사용할 수 있다.
 ```py
import matplotlib.pyplot as plt
plt.rc('font', family = 'NamumBarunGothic')
 ```

 ### 기간 중 가장 많이 차트에 곡을 올린 태연의 노래 조회 건수
 ```py
 df_tae = df[df['아티스트']=='태연']
 df_tit = df_tae.groupby('곡')[['아티스트']].count
 ```

 ### 아티스트와 곡 입력받았을 때 순위 변화 그래프 출력
 ```py
 plt.style.use('ggplot')

 for tit in df_tae['곡'].unique():
     df_title = df[df['곡'] == tit]
     plt.plot(df_title.날짜, df_title.점수, label = tit)

plt.legend() ; plt.show()
