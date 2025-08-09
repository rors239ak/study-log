import random

# サイコロを10回振る
results = [random.randint(1, 6) for _ in range(10)]

print("サイコロの結果:", results)
print("合計:", sum(results))
print("平均:", sum(results) / len(results))
