############## time out ###############
N = int(input())
card1 = input().split()

M = int(input())
card2 = input().split()

card1 = list(map(int, card1))
card2 = list(map(int, card2))

def compare(val):
      return 1 if val in card1 else 0
                  
for i in map(compare, card2):
      print(i, end=' ')
