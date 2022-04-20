from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing.text import Tokenizer

# 문자에 대한 정수 인코딩!
# 전처리와 불용어 처리를 끝낸 X_train과 X_test 필요
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing.text import Tokenizer

# okenizer.word_index  : X_train 의 word index 값들을 확인할 수 있다.
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)
print(tokenizer.word_index)

threshold = 3
total_cnt = len(tokenizer.word_index) # 단어의 수
rare_cnt = 0                  # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
total_freq = 0                # 훈련 데이터의 전체 단어 빈도수 총 합
rare_freq = 0                 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

# 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
for key, value in tokenizer.word_counts.items():
    total_freq = total_freq + value

    # 단어의 등장 빈도수가 threshold보다 작으면
    if(value < threshold):
        rare_cnt = rare_cnt + 1
        rare_freq = rare_freq + value

print('단어 집합(vocabulary)의 크기 :',total_cnt)
print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s'%(threshold - 1, rare_cnt))
print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)

# 전체 단어 개수 중 빈도수 2 이하인 단어 개수는 제거
vocab_size = total_cnt - rare_cnt +2
print('단어집합의 크기 : ', vocab_size)

tokenizer = Tokenizer(vocab_size, oov_token = 'OOV') 
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

print(X_train[:3]) # 결과를 확인해보면, 단어들이 숫자로 대체되어 출력되는 걸 볼 수 있다.

y_train = np.array(train_data['label'])
y_test = np.array(test_data['label'])

# 빈 샘플을 제거
drop_train = [index for index, sentence in enumerate(X_train) if len(sentence) < 1]
print(drop_train[:3])  # 드롭되는 데이터를 출력해줌

X_train = np.delete(X_train, drop_train, axis=0)
y_train = np.delete(y_train, drop_train, axis=0)
print(len(X_train))
print(len(y_train))


# 리뷰에 사용되는 단어의 갯수에 대한 시각화
print('리뷰의 최대 길이 :',max(len(l) for l in X_train))
print('리뷰의 평균 길이 :',sum(map(len, X_train))/len(X_train))
plt.hist([len(s) for s in X_train], bins=50)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()


# 위의 plt를 확인해본 뒤 아래 함수를 실행해보면 분포 파악에 도움이 됨.
def below_threshold_len(max_len, nested_list):
  cnt = 0
  for s in nested_list:
    if(len(s) <= max_len):
        cnt = cnt + 1
  print('전체 샘플 중 길이가 %s 이하인 샘플의 비율: %s'%(max_len, (cnt / len(nested_list))*100))



## 이후 시퀀스 패딩에 대한 내용이 있는데.. 아직 잘 모르는 내용이라 추후에 추가하겠슴!
