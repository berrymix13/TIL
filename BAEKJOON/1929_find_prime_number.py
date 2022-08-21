## finde M <= prime number <= N
m, n = map(int, input().split())
for i in range(m, n+1):
    if i <= 7:
        if i in [2, 3, 5, 7]:
            print(i)
    else:
      lst=[i%j for j in [2, 3, 5, 7]]
      if 0 not in lst:
           print(i)

