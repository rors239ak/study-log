def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


arr = [212, 533, 1221, 121,5535, 7, 975, 70]
print(f"ソート前：{arr}")
print(f"ソート後：{bubble_sort(arr)}")