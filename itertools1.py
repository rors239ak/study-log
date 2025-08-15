import itertools

# 人の組み合わせを作成
people = ["A", "B", "C", "D", "E", "F", "G"]

# 2人組の組み合わせ
pairs = list(itertools.combinations(people, 2))
len_pairs = len(pairs)
print("2人組の組み合わせ:", pairs)
print(f"2人組は{len_pairs}通り")

