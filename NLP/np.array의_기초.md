## np.array의 이해

```python
import numpy as np
arr = np.arrange(0, 20, 2)
print(arr)
```

> [0 2 4 6 8 10 12 14 16 18]

보기에는 리스트처럼 생겼지만, 리스트와는 다르게 콤마가 없음을 확인할 수 있다.

인덱싱을 통해 요소만을 뽑아낼 수 있고, True/False로 구성된 boolean 배열을 기준으로 결과를 출력할 수 있다.

```python
print(arr >= 10)
print(arr[arr >= 10])
```

> [False False False False False  True  True  True  True  True] 
>
> [10 12 14 16 18]



0이 아닌 값만을 출력할 때에는 `np.nonzero(arr)`함수를 통해 쉽게 뽑아낼 수 있다.

```python
## 0이 아닌 값만 출력
arr[[3, -1]]=0  # arr의 3번째, -1번째 값을 0으로 변경
print(arr)
print(np.nonzero(arr))
```

> [ 0  2  4  0  8 10 12 14 16  0] 
>
> (array([1, 2, 4, 5, 6, 7, 8]),)

#### 행렬 곱 (dot)

```python
import numpy as np
arr1 = np.array([1,3,5])
arr2 = np.array([2,4,6])
```

```python
np.dot(arr1, arr2.T)
```

> ```python
> array([[17],
>        [39]])
> ```





### 배열 합치기

```python
arr1 = np.arange(1, 5).reshape(2, -1)
arr2 = np.array([5, 6]).reshape(1, 2)

print(arr1)
print(arr2)
```

>```python
>[[1 2]
> [3 4]] 
>
>[[5 6]]
>```



```python
# 아래로 이어붙임
print(np.concatenate((arr1, arr2), axis=0), "\n")
```

> ```python
> [[1 2]
>  [3 4]
>  [5 6]] 
> ```



```python
# 옆으로 병합
print(arr2.T)
print(np.concatenate((arr1, arr2.T), axis=1), "\n")
```

> ```python
> [[5]
>  [6]]
> 
> [[1 2 5]
>  [3 4 6]] 
> ```

#### numpy 입출력

- np.save(file, arr) => array 1개를 파일로 저장(바이너리)

- np.savez(file, arr1, arr2) => 복수 배열을 파일로 저장(바이너리)



- np.load(file)  => 배열 형식으로 저장된 데이터 불러오기

- np.savetxt()  => 텍스트 형식으로 배열값 저장

- np.loadtxt()  => 텍스트 형식으로 저장된 배열값 불러오기