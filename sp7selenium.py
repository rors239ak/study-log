#見られちゃいけないパスワード隠すためのモジュール
from dotenv import load_dotenv
#urlとかを取ってくるためのモジュール、サーバーに負担をかけないためのモジュール、メール送信のためのモジュール
import time, yagmail, os
#相対パスを絶対パスに変換するモジュール
from urllib.parse import urljoin
#画面を直接動かすセレニウムモジュール
from selenium import webdriver
from selenium.webdriver.common.by import By
#セレニウム用のエラー処理モジュール
from selenium.common.exceptions import NoSuchElementException

keyword1 = input("①こだわりを単語で1つ入力してください")
keyword2 = input("②こだわりを単語で1つ入力してください")
keyword3 = input("③こだわりを単語で1つ入力してください")
#クロームをバックエンドのみで作動するようにする
options = webdriver.ChromeOptions()
options.add_argument("--headless")

#クロームで運転するよって感じ
driver = webdriver.Chrome(options=options)













#スクレイピング始めるurl
url = "https://xn--pckua2a7gp15o89zb.com/adv/?keyword=IT&area=%E7%A6%8F%E5%B2%A1%E5%B8%82%E6%97%A9%E8%89%AF%E5%8C%BA%20or:%E7%A6%8F%E5%B2%A1%E5%B8%82%E5%9F%8E%E5%8D%97%E5%8C%BA%20or:%E7%A6%8F%E5%B2%A1%E5%B8%82%E4%B8%AD%E5%A4%AE%E5%8C%BA%20or:%E7%A6%8F%E5%B2%A1%E5%B8%82%E8%A5%BF%E5%8C%BA%20or:%E7%A6%8F%E5%B2%A1%E5%B8%82%E5%8D%9A%E5%A4%9A%E5%8C%BA&e=1&p=3&pl=3000000&pu=4000000&u=3"#ここは求人ボックスの自分の好きなURLを設定してね！












#スタート地点の地図渡す感じ
driver.get(url)
#本文に入れるための枠
body = []
#被り防止
seen_companys = set()
#全ページ終わるまで
while True :
  #全ての求人先をひとくくりにしたもの
  all_ = driver.find_elements(By.CLASS_NAME, "p-result_card")
  #①ここから下の①までで１ページ分----------------------------------------------
  #求人の一個をクリックして詳細を見る感じ
  for one in all_:
    try:#環境的に重かったりした場合エラーで終わらせるのではなくcontinueで次にスキップ
      one1 = one.find_element(By.CLASS_NAME, "p-result_title--ver2")
      one1.click()
      time.sleep(1)
      #会社名を取り出す
      company_tag = one.find_element(By.CLASS_NAME,"p-result_company")
      company = company_tag.text
      #日付を取り出す
      through_list = ["1日前", "2日前", "3日前", "4日前", "5日前"]
      day_tag = one.find_element(By.CLASS_NAME,"p-result_updatedAt_hyphen")
      #5日以内の求人だったら
      if day_tag.text in through_list or "時間前" in day_tag.text:
      #linkを取り出す
        base_url = "https://xn--pckua2a7gp15o89zb.com"
        link_tagu = one.find_element(By.CSS_SELECTOR,"h2 a")
        link = urljoin(base_url, link_tagu.get_attribute("href"))
        #こだわりを取り出す
        new_one = driver.find_element(By.CLASS_NAME, "p-preview_inner")
        kodawari_tags = new_one.find_elements(By.CSS_SELECTOR, "section ul li.p-result_tag_feature--ver3")
        #こだわりのリスト
        kodawari_tag = [kodawari.text for kodawari in kodawari_tags]
        #リストをまとめた文字列に変える
        kodawari = "、".join(kodawari_tag)       
        #福岡限定で探す
        place_tag = new_one.find_element(By.CLASS_NAME, "p-detail_summary")
        place = place_tag.text











        #NGワードが入っていたらcontinueするための準備
        # ここは自分の好きなワード入れてね！！
        ng_words = ["未経験OK"]
        must_words = [ "基本情報技術者"]













        new_body = driver.find_element(By.CSS_SELECTOR, "div.p-preview_body.s-preview-body")
        # NGワードが本文に1つでも含まれているか福岡以外なら求人全体をスキップするようにする
        if any(ng in new_body.text for ng in ng_words) or "福岡" not in place: 
          continue
        if any(must in  new_body.text for must in must_words):  
          #seen_companysというリストに会社名がかぶってなければappendしていく
          if company not in seen_companys:
            seen_companys.add(company)
            #入力したキーワードが含まれている場合(lowerで大文字小文字も関係なく認識可能)
            if keyword1.lower() in [k.lower() for k in kodawari_tag] or keyword2.lower() in [k.lower() for k in kodawari_tag]or keyword3.lower() in [k.lower() for k in kodawari_tag]:
              # 会社名とこだわりとリンクをbodyという最初に用意しといたリストに追加
              body.append((f"{company}\n{kodawari}\n{link}\n\n"))
              print(f"{company}\n{kodawari}\n{link}\n")
    except: continue    
  #①ここまでで１ページ分を繰り返す----------------------------------------------
  #次のページに行く、そしてまた①を繰り返す
  try:
    click = driver.find_element(By.CLASS_NAME, "c-pager_btn_in.c-pager_btn--next")
    click.click()
    time.sleep(1)

    #全ページ読み込んだ場合こうなるのでwhileの終着点
  except NoSuchElementException:
    print("全ページ読み込み完了")
    break
#メール送信
#本文(条件分岐)
if body:#bodyはリストなので全部くっつけて文字列に変更
    honbun = "".join(body)
else:
    honbun = "今日は該当する求人が見つかりませんでした"












 #メールを送るための下準備
my_email = "me"#送り元例
your_email = "your"#送り先例
 # 送り元と送り先はどっちも同じ自分のメールアドレスでもOK













load_dotenv()#.envファイルを読み込む
apripw = os.getenv("APRIPW")#見せちゃダメなパスワードをとりだす
#自分のメールアドレスとアプリパスワードでGmailアカウントでログインする処理
yag = yagmail.SMTP(my_email, apripw)
#件名
subject = "今日の新着求人情報"
#送信作業
yag.send(to=your_email, subject=subject, contents=honbun)
#確認作業
print("メール送信完了")

