# ユーザーからの入力を受け取る
numbers_str = input("整数をカンマ区切りで入力してください: ")

# 文字列を分割して整数に変換
numbers = [int(num.strip()) for num in numbers_str.split(",")]

# 昇順にソート
numbers.sort()

# 合計値を計算
total = sum(numbers)

# 結果を表示
print("昇順:", numbers)
print("合計値:", total)
