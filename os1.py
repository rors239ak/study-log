import os

# "."で現在のディレクトリにあるファイルを表示
files = os.listdir(".")
print("このフォルダの中身:")
for f in files:
    print("-", f)
