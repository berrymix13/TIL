# number of test Data = T
# number of Floors,  numer of Rooms, N th guest = H, W, N


############# my code #############
T = int(input())
result=[]
for _ in range(T):
      lst = [int(i) for i in input().split()]
      H = lst[0]; W = lst[1]; N = lst[2]

      Room = [b*100+a for a in range(1, W+1) for b in range(1, H+1)]
      print(Room[N-1])


############# Ref code : woosungko #############
t = int(input())

for i in range(t):
    h, w, n = map(int, input().split())
    num = n//h + 1
    floor = n % h
    if n % h == 0:
        num = n//h
        floor = h
    print(f'{floor*100+num}')
