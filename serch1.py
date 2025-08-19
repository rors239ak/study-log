import random

def linear_search(arr, key):
    for i in range(len(arr)):
        if arr[i] == key:
            return i  # 見つかったインデックスを返す
    return -1  # 見つからない場合

nums = []
for i in range(1, 20):
    nums.append(random.randint(1, 50))
print(nums)
print(linear_search(nums, 30))  
