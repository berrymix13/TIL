#################################################
#
# 한국어 감성사전을 이용한 감정분석
#
#################################################
import json
import pandas as pd
from tqdm import tqdm

### 감정사전 파일 읽어오기
SentiWord = pd.read_json('./data/SentiWord_info.json')
print(SentiWord.head(10))

# '희귀'라는 단어가 있는지 검색
print(SentiWord[SentiWord.word_root == '희귀'])

## 없으므로 추가하고 저
# 방법 1  : append
SentiWord = SentiWord.append({'word':'희귀하다', 'word_root':'희귀','polarity':1}, ignore_index = True)
SentiWord.to_csv('./data/SentiWord_info.csv', index = False)

# 방법2  : df.loc[len(df)]를 통해 리스트 형태로 행 삽입
SentiWord.loc[len(SentiWord)] = ['합의하다', '합의', 1]
SentiWord.loc[len(SentiWord)] = ['징용되다', '징용', -2]


### 데이터를 입력받아 긍정/ 부정 분석
#
# -  단어를 입력받은 후 긍정과 부정을 전달해주는 함수 생성
#     - 만약 단어가 사전에 존재하지 않을 경우, 0으로 반환
def pos_neg(word):
    tmp=SentiWord[(SentiWord['word']==word) | (SentiWord['word_root']==word)]
    try:
        word_res=(word, tmp['polarity'][tmp.index[0]])
    except:
        word_res=(word, 0)
        
    return word_res

