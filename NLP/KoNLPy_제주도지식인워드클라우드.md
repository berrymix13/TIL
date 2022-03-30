## 한국어 형태소 분석

JVM와 Jpype를 설치한 뒤

`!pip install konlpy` 를 진행해준다.

```python
from konlpy.tag import Okt

okt = Okt()
okt.nouns('안녕 하세요. 방탄소년단입니다.')
```

> ['안녕', '방탄소년단']

Okt() 외에도 Kkma()를 쓸 수 있고, 결과는 조금 다르다.

Mecab은 Windows에서 쓸 수 없다.

```python
okt.morphs('안녕 하세요. 방탄소년단입니다.')
```

> ['안녕', '하세요', '.', '방탄소년단', '입니다', '.']

## 지식인 질문, 답변 형태소 분석

먼저 저번에 저장한 제주도 지식인 csv를 읽어들인다.

```python
from konlpy.tag import Okt
from nltk import Text # NLTK text로 만들 때 사용.
from collections import Counter # 단어 개수 세어줌
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import nltk
from tqdm import tqdm
```

1. csv 파일 읽어오기

   ```python
   kin_df = pd.read_csv('c:/pydata/제주도_지식인.csv')
   kin_df.head(3)
   ```

   질문 df와 답변df로 나누어 저장한다.

   ```python
   quesDf = kin_df[['질문']]
   ansDf = kin_df[['답변']]
   ```

2. 데이터 프레임의 각 행을 (단어, 품사) 형태로 리스트에 저장하는 함수 생성

   ```python
   okt = Okt()
   def pos_text(dataframe):
       
       pos_txt_all = []
       for i in tqdm(dataframe.index):
           try:
               pos_txt = okt.pos(dataframe.iloc[i,0]) 
               pos_txt_all += pos_txt
           except:
               continue
       
       return pos_txt_all
   ```

   - `okt.pos()`   :  튜플 형태로 (단어,품사)를  알려주며, 최종적으로 리스트로 반환해준다.
   - 따라서 `pos_txt_all`을 통해 하나의 리스트에 전부 넣어주었다.
   - 답변에 숫자 때문에 나는 오류를 처리하기 위해 try를 사용했다. (덕분에 오래걸린듯)

 3. 반환된 리스트에서 명사, 동사, 형용사만을 추출해 Text로 만들어주는 함수 생성

    ```python
    def make_morph(pos_txt_all):
        # 명사
        noun = [t[0] for t in pos_txt_all if t[1] == 'Noun']
        # 동사
        verb = [t[0] for t in pos_txt_all if t[1] == 'Verb']
        # 형용사
        adjs = [t[0] for t in pos_txt_all if t[1] == 'Adjective']
    
        morph = noun + verb + adjs
        morph = Text(morph)
        
        return morph
    ```

 4.  위의 두 함수 실행

    ```python
    # 질문
    pos_txt_all_Q = pos_text(quesDf)
    print(len(pos_txt_all_Q))
    # 답변
    pos_txt_all_A = pos_text(ansDf)
    print(len(pos_txt_al_A))
    ```

    > 48996
    >
    > 1598905

    ```python
    # 질문
    morphQ = make_morph(pos_txt_all_Q)
    print(morphQ[:10])
    
    # 답변
    morphA = make_morph(pos_txt_all_A)
    morphA[:10]
    ```

    > ['결혼식', '예비신랑', '신혼여행', '제주도', '가게', '그때', '제주도', '날씨', '요', '꽃']
    >
    > ['사람', '라면', '팔', '바람막이', '옷', '하나', '가세', '주먹', '크기', '옷']

 5.  불용어 걸러내기

    사전에 저장했던 한국어 불용어 파일을 읽어들인다.

    ```python
    f = open('c:/pydata/stop_words_ko.txt', encoding = 'utf-8')
    stopwords = f.read()
    f.close()
    
    stop_words = stopwords.split("\n")
    print(stop_words[:10])
    ```

    > ['', '아', '휴', '아이구', '아이쿠', '아이고', '어', '나', '우리', '저희']

    ```python
    stop_words.extend(['제주도','곳','박','처음'])
    ```

    ```python
    morphQ_sw = [ sw for sw in morphQ if sw not in stop_words]
    morphA_sw = [ sw for sw in morphA if sw not in stop_words]
    
    print(morphQ_sw[:10])
    print(morphA_sw[:10])
    ```

    > ['결혼식', '예비신랑', '신혼여행', '가게', '날씨', '꽃', '여자친구', '여행', '여행', '코스']
    >
    > ['사람', '라면', '바람막이', '옷', '가세', '주먹', '크기', '옷', '질문', '날씨']

 6. 빈도수 계산

    ```python
    morphQ_cnt = Counter(morphQ_sw) 
    morphA_cnt = Counter(morphA_sw) 
    ```

    - `.most_common()`   :  딕셔너리형 자료를 튜플 구조로 만들어 리스트 형태로 제공. 빈도수대로 정렬해준다.

    ```python
    morphQ_txt = morphQ_cnt.most_common()   
    print(morphQ_txt[:20])
    
    morphA_txt = morphA_cnt.most_common()   
    print(morphA_txt[:20])
    ```

    > [('여행', 712), ('추천', 406), ('코스', 218), ('렌트카', 216), ('숙소', 182), ('질문', 170), ('맛집', 140), ('합니다', 133), ('가족', 126), ('계획', 119), ('할', 119), ('친구', 115), ('갈', 114), ('있는', 114), ('렌트', 112), ('가는데', 110), ('좋은', 106), ('정도', 104), ('예정', 101), ('없음', 101)]
    >
    > [('제주', 17078), ('해안', 11816), ('관람', 10672), ('제주시', 10029), ('원', 9568), ('여행', 8551), ('있는', 8473), ('코스', 7477), ('해변', 7230), ('추천', 6792), ('무료', 6712), ('도로', 6255), ('서귀포', 5621), ('숙소', 5459), ('체험', 5319), ('정도', 5289), ('서귀포시', 5075), ('바다', 4975), ('방법', 4782), ('어린이', 4723)]

    - 빈도수가 낮은 데이터 (20) 미만 제거

    ```python
    morphQ_txt_up = [tc for tc in morphQ_txt if tc[1] >= 20] 
    morphA_txt_up = [tc for tc in morphA_txt if tc[1] >= 20] 
    ```

    - 워드클라우드 작업을 위해 딕셔너리 구조로 변경.

    ```python
    morphQ_txt_up = dict(morphQ_txt_up)
    morphA_txt_up = dict(morphA_txt_up)
    ```

### 워드클라우드 출력

```python
# 워드 클라우드 틀 셋팅
wordcloud = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf', background_color= 'white', width=700, height=700,
                      max_words = 100, max_font_size=200)

# 딕셔너리 구조의 데이터를 이용해 워드 클라우드 출력
wc =  wordcloud.generate_from_frequencies(morphQ_txt_up)
plt.figure(figsize = (6,8))
#plt.imshow(wc)
#interpolation은 이미지를 어떻게 처리해서 보여줄지 결정합니다. bilinear는 부드럽게
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()
```

```python
wordcloud = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf', background_color= 'white', width=700, height=700,
                      max_words = 100, max_font_size=200)

# 딕셔너리 구조의 데이터를 이용해 워드 클라우드 출력
wc =  wordcloud.generate_from_frequencies(morphA_txt_up)
plt.figure(figsize = (6,8))
#plt.imshow(wc)
#interpolation은 이미지를 어떻게 처리해서 보여줄지 결정합니다. bilinear는 부드럽게
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()
```

