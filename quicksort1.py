def quick_sort(arr):
    # 要素が1個以下ならそのまま返す
    if len(arr) <= 1:
        return arr

    # 基準値（pivot）をリストの先頭から選ぶ
    pivot = arr[0]

    # pivot より小さい値のリスト
    left = [x for x in arr[1:] if x <= pivot]
    # pivot より大きい値のリスト
    right = [x for x in arr[1:] if x > pivot]

    # 再帰的にソート
    return quick_sort(left) + [pivot] + quick_sort(right)


if __name__ == "__main__":
    numbers = [5, 3, 8, 6, 2, 7, 4, 1]
    print("ソート前:", numbers)
    sorted_numbers = quick_sort(numbers)
    print("ソート後:", sorted_numbers)
