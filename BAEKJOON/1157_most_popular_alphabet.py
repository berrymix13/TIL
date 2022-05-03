# 알파벳 대소문자로 된 단어가 주어지면,
# 이 단어에서 가장 많이 사용된 알파벳이 무엇인지 알아내는 프로그램
# 대소문자 구분 X

a = input()
a = a.lower()

lst = [a[v] for v in range(len(a))]
lst = list(set(lst))

cnt = [a.count(i) for i in lst]
max_n = max(cnt)

if cnt.count(max_n) > 1:
      print('?')
else:
      idx = cnt.index(max_n)
      print(max(lst[idx].upper()))
