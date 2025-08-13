import requests
import json

# 無料で使えるサンプルAPI（ダミーデータ）
url = "https://api.sampleapis.com/weather/forecast"

# APIへリクエストを送信
response = requests.get(url)

# レスポンス（結果）のステータス確認
if response.status_code == 200:
    data = response.json()  # JSON形式をPythonの辞書に変換
    print("データ取得成功！")

    # データの一部を表示（例: 最初の1件）
    print(json.dumps(data[0], indent=2, ensure_ascii=False))
else:
    print("データ取得失敗:", response.status_code)
