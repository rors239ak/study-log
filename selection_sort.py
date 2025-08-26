def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i+1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

arr = [857, 244, 977, 22, 978, 112, 9687, 7474, 7365]
print(f"ソート前：{arr}")
print(f"ソート後：{selection_sort(arr)}")