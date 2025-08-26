import random

def heapify(arr, n, i):
    largest = i        # 親ノード
    left = 2 * i + 1   # 左の子
    right = 2 * i + 2  # 右の子

    # 左の子と比較
    if left < n and arr[left] > arr[largest]:
        largest = left

    # 右の子と比較
    if right < n and arr[right] > arr[largest]:
        largest = right

    # 最大値が親じゃなければ入れ替え
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)  # 再帰的に調整

def heap_sort(arr):
    n = len(arr)

    # ヒープを構築
    for i in range(n//2 - 1, -1, -1):
        heapify(arr, n, i)

    # ヒープから要素を一つずつ取り出す
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # ルート（最大）と最後を交換
        heapify(arr, i, 0)               # ヒープを再構築

    return arr

arr = []
for i in range(1, 20):
    arr.append(random.randint(1, 1000))
print(f"ソート前：{arr}")
print(f"ソート後：{heap_sort(arr)}")