import re

text = "連絡先: yamada@gmail.com または info@gmail.co.jp にメールしてください"
pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

emails = re.findall(pattern, text)
print("見つかったメールアドレス:", emails)
