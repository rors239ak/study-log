import math

# sqrt平方根
num = 16
print(f"{num} の平方根:", math.sqrt(num))

# 円の面積（半径5） powでradius(半径) 第2引数で2乗か
radius = 5
area = math.pi * math.pow(radius, 2)
print(f"半径 {radius} の円の面積:", area)
