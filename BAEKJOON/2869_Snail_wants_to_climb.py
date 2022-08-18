# 2869_Snail wants to Climb
# A = climb / B = fall / V = bar meter
# timeout 0.15 seconds

A, B, V = map(int, input().split())

st = time.time()
res = (V-B) // (A-B)

if (V-B) % (A-B) != 0:
      res +=1
      
print(res)
