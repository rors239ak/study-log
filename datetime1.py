from datetime import datetime, timedelta

# 今日の日付
today = datetime.now()
print("今日:", today.strftime("%Y-%m-%d %H:%M:%S"))

# 7日後   timedelta:日付の加減算
seven_days_later = today + timedelta(days=7)
print("7日後:", seven_days_later.strftime("%Y-%m-%d"))
