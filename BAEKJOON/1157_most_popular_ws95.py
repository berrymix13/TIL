a = input()
a = a.upper()
set_a = set(a)
num = []
for i in set_a:
    num.append(a.count(i))
ans = max(num)
if num.count(ans)>1:
    print("?")
else:
    print(list(set_a)[num.index(max(num))])
