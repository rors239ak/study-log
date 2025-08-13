import numpy as np

# 0〜9までの配列を作成
arr = np.arange(1, 11)
print("元の配列:", arr)

# 偶数だけ取り出す
even_arr = arr[arr % 2 == 0]
print("偶数だけ:", even_arr)

# 配列を2倍
double_arr = arr * 2
print("2倍した配列:", double_arr)

# 配列の形を変える（reshape）
reshaped_arr = arr.reshape(2, 5)
print("形を変えた配列:\n", reshaped_arr)

# ランダムな小数の配列を作って平均・合計を計算
rand_arr = np.random.rand(3, 4)
print("ランダム配列:\n", rand_arr)
print("   平均:", np.mean(rand_arr))
print("   合計:", np.sum(rand_arr))
