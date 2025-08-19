import random

def binary_search(arr, key):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            left = mid + 1
        else:
            right = mid - 1
    return -1

nums = []
for i in range(1, 20):
    nums.append(random.randint(1, 50))
print(nums)
print(binary_search(nums, 30))  
