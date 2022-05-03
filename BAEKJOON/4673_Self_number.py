# 생성자 리스트 : [(n,d(n)]
# 100 = 100 + 1 + 0 + 0
def d(n):
      num = n
      for i in range(len(str(n))):
            num += int(str(n)[i])
      return num

self_lst = [n for n in range(1,10001)]
for j in range(1, 10001):
      if d(j) in self_lst:
            self_lst.remove(d(j))
            
for val in self_lst:
      print(val)


