from collections import Counter

fruits = ["apple", "banana", "apple", "orange", "banana", "apple"]
count = Counter(fruits)

print("フルーツの出現回数:", count)
print("一番多いフルーツ:", count.most_common(1))
