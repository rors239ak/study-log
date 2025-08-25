import random

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key
    return arr


arr = []
for i in range(1, 20):
    arr.append(random.randint(1, 1000))
print(f"ソート前：{arr}")
print(f"ソート後：{insertion_sort(arr)}")
