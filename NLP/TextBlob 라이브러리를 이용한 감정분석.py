#!/usr/bin/env python
# coding: utf-8

# ### TextBlob 라이브러리
# - 익숙한 인터페이스를 통해 일반적인 텍스트 처리 작업에 대한 액세스를 제공
# - TextBlob 객체를 자연어 처리를 수행하는 방법을 학습 한 Python 문자열 인 것처럼 처리 할 수 있다.
# - 참조: https://textblob.readthedocs.io/en/latest/quickstart.html#translation-and-language-detection

# In[3]:


#!pip install textblob


# In[1]:


from textblob import TextBlob
import pandas as pd
import numpy as np


# In[2]:


# 문장 입력
txt1 = TextBlob('맥주가 좋았습니다.')
txt2 = TextBlob('I love Beer')


# In[3]:


# TextBlob 모듈을 이용한 언어 확인
print(txt1.translate(to = 'en'))
print(txt1.translate(to = 'ja'))
print(txt2.translate(to = 'ja'))


# ### 텍스트 감정 분류기 만들기
# - 학습 데이터(train) : 문장과 긍정/ 부정 마킹
# - 학습데이터로 학습하고 긍부정 분류
# - 평가데이터(test)

# In[4]:


from textblob.classifiers import NaiveBayesClassifier

# 학습 데이터 세트
train = [ ('I love this sandwich.', 'pos'), 
        ('This is an amazing place!', 'pos'), 
        ('I feel very good about these beers.', 'pos'), 
        ('This is my best work.', 'pos'), 
        ("What an awesome view", 'pos'), 
        ('I do not like this restaurant', 'neg'), 
        ('I am tired of this stuff.', 'neg'), 
        ("I can't deal with this", 'neg'), 
        ('He is my sworn enemy!', 'neg'), 
        ('My boss is horrible.', 'neg')]


# In[5]:


## 테스트 세트
test = [('The beer was good.', 'pos'),
        ('I do not enjoy my job', 'neg'),
        ("I ain't feeling dandy today.", 'neg'),
        ("I feel amazing!", 'pos'),
        ('Gary is a friend of mine.', 'pos'),
        ("I can't believe I'm doing this.", 'neg')]


# In[6]:


### NaiveBayesClassifier 개체에 학습 데이터를 입력하고 긍정(pos)/부정(neg) 모델 생성
pos_neg = NaiveBayesClassifier(train)
pos_neg


# In[7]:


pos_neg.classify('Gary is a friend of mine')


# In[12]:


for text in test:
    print(f'{text} : {pos_neg.classify(text[0])}')


# In[17]:


print(f'정확도  : {5/6}\n오차비율  : {1/6}')


# In[18]:


# 긍정에 대한 정밀도
print(f'정밀도  : {2/2}')


# In[19]:


# 부정에 대한 정밀도
print(f'정밀도  : {3/4}')


# In[ ]:


# 재현율  : 실제 긍정중 예측 긍정


# In[ ]:





# In[21]:


# TextBlob 객체를 사용하여 여러 문장으로 구성된 텍스트도 분류
tag2 = TextBlob("The beer was amazing. But the hangover was horrible. My boss was not happy.",
         classifier=pos_neg)
print(tag2.classify())


# In[26]:


## 데이터 분리
#  알아서 마침표를 기준으로 분리 됨. 
tag2.sentences


# In[29]:


for text in tag2.sentences:
    print(f'{text}\t: {text.classify()}')


# In[30]:


# 정확도
acc = pos_neg.accuracy(test)
print(acc)


# In[31]:


# 정확도보단 재현율, 정밀도를 많이 쓰게됨..
print(pos_neg.show_informative_features())


# ### 한글 긍부정 처리

# In[32]:


from textblob import TextBlob as tb
from textblob.classifiers import NaiveBayesClassifier


# In[35]:


train = [('나는 이 샌드위치를 정말 좋아해.', '긍정'),
         ('정말 멋진 곳이에요!', '긍정'),
         ('나는 이 맥주들이 아주 좋다고 생각해요.', '긍정'),
         ('이것은 나의 최고의 작품입니다.', '긍정'),
         ("정말 멋진 광경이다", "긍정"),
         ('난 이 식당 싫어', '부정'),
         ('난 이게 지겨워.', '부정'),
         ("이 문제는 처리할 수 없습니다.", "부정"),
         ('그는 나의 불구대천의 원수이다.', '부정'),
         ('내 상사는 끔찍해.', '부정'),
         ('나는 내 꿈을 믿는다', '긍정'),
         ('나는 매일 최선을 다하고 있다', '긍정'),
         ('나는 있는 그대로의 나를 사랑한다', '긍정'),
         ('나는 내 삶을 100% 책임진다', '긍정'),
         ('가장 좋은 일은 아직 생기지 않았다', '긍정'),
         ('나는 매일 나의 삶에 감사한다', '긍정'),
         ('새로나온 휴대폰은 배터리 교체가 되지 않아 불편하다', '부정'),
         ('이번에 나온 영화 너무 재밌다. 주말에 또 보고 싶다.', '긍정'),
         ('나의 아버지는 이해가 안된다', '부정'),
         ('나는 어머니와 있을 때 퉁명해진다', '부정'),
         ('나는 어머니와 있을 때 불편할 때가 있다.', '부정'),
         ('치킨집에 선결제로 주문했는데 돈은 결제가 되었는데 치킨집에선 주문이 안들어왔다고합니다.', '부정'),
         ('지금 현재 네이버 실시간 검색어에 떴고, 여전히 고객센터는 전화연결이 되지않습니다. ', '부정'),
         ('이럴거면 요기요처럼 아예 접속도 안되게하던가 결제를 막았어야하는데', '부정'),
         ('결제해서 가게에 돈 준 것도 아니고 본인들이 가져가놓고 전화도 안받으면 돈은 어떻게 돌려받습니까?', '부정'),
         ('너무 유용하고 편리하네요.. ', '긍정'),
         ('처음 구입한다고 쿠폰 받고 이용하니깐 저렴하게 먹을 수 있었고 배달시간도 만족스러워서 좋았습니다.', '긍정'),
         ('배달의 민족 강추 합니다. ', '긍정'),
         ('자주 이용할께요ㅡㅡㅡ강추 강추!!!', '긍정')]


# In[36]:


test = [('맥주가 좋았습니다.', '긍정'),
        ('난 내 일을 즐기지 않는다', '부정'),
        ('오늘은 기분이 안 좋아요.', '부정'),
        ('빠른 배달 좋네요', '긍정'),
        ('네드는 나의 친구입니다.', '긍정'),
        ('제가 이렇게 하고 있다니 믿을 수가 없어요.', '부정')]


# In[37]:


pos_neg = NaiveBayesClassifier(train)
pos_neg


# In[38]:


pos_neg.accuracy(test)


# ### 배민 앱 사용 후기를 이용한 긍부정 모델 생성

# In[39]:


import pandas as pd
from textblob import TextBlob as tb
from textblob.classifiers import NaiveBayesClassifier


# In[45]:


df = pd.read_csv('./data/배민어플후기.csv', encoding= 'cp949')
df.columns = ['Reviews', 'pos_neg']
df.head(3)


# In[52]:


df.isna().sum()


# In[53]:


df.info()


# In[59]:


df[(df.pos_neg == '긍정')|(df.pos_neg == '부정')]


# In[60]:


df_nan = df[df.pos_neg.isnull()]
df_nan


# In[63]:


df2 = df.dropna()
df2.isna().sum()


# ### train/test 데이터 생성 (75 : 25)

# In[71]:


df_pos = df2[df2.pos_neg == '긍정']
df_neg = df2[df2.pos_neg == '부정']

print(df_pos.shape)
print(df_neg.shape)

# groupby 로도 확인 가능.


# In[72]:


## 긍부정 데이터 동일하게 맞추기

df_neg = df_neg.sample(784)
print(df_pos.shape)
print(df_neg.shape)


# In[74]:


print('train : ',784 * 0.75)
print('test  : ',784 * 0.25)


# In[94]:


train = pd.concat([df_pos[:589],df_neg[:589]])
train.shape


# In[95]:


test = pd.concat([df_pos[589:],df_neg[589:]])
test.shape


# In[97]:


# 데이터 순서를 랜덤하게
train_df = train.sample(1178).reset_index(drop = True)
display(train_df.head())

test_df = test.sample(390).reset_index(drop = True)
test_df.head()


# In[98]:


# 튜플구조 만들기
def to_tuple(df_t):
    lst = []
    for i in df_t.index:
        lst.append((df_t.iloc[i,0],df.iloc[i,1]))
    return lst


# In[99]:


train = to_tuple(train_df)
train[:3]


# In[100]:


test = to_tuple(test_df)
test[:3]


# In[103]:


from textblob import TextBlob as tb
from textblob.classifiers import NaiveBayesClassifier

pos_neg = NaiveBayesClassifier(train)
test_acc = pos_neg.accuracy(test)

print(f'정확도  : {test_acc}')
pos_neg


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




