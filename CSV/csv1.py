import csv

# 書き込み
with open("csv1.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["名前", "年齢"])
    writer.writerow(["平野", 32])
    writer.writerow(["森", 25])

# 読み込み
with open("csv1.csv", mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
