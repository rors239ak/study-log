import random

nums = []
for i in range(1, 20):
    nums.append(random.randint(1, 50))
print(nums)
print("最大値:", max(nums))
print("最小値:", min(nums))
