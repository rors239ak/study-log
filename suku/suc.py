# 同一フォルダ内の images フォルダに、選択中の id/class に一致する画像を最大 7 枚保存するスクリプト
# 実行時に検索ワード・id 部分文字列・class 部分文字列 をシェル経由で input() で入力します。
# 使い方: python suc.py
# 依存: selenium, webdriver-manager, requests
# python -m pip install --upgrade selenium webdriver-manager requests

import time
import requests
import mimetypes
from pathlib import Path
from urllib.parse import quote
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

MAX_RUNTIME = 60  # 全体タイムリミット（秒）
SAVE_MAX = 7      # デフォルト保存枚数（変更なし、いちいち聞かない）

def build_google_images_url(query: str) -> str:
    return f"https://www.google.com/search?tbm=isch&q={quote(query)}"

def collect_target_image_urls(query, match_id_substr, match_class_substr, max_count, headed=True, deadline=None):
    opts = Options()
    if not headed:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1366,900")
    opts.add_argument(f"user-agent={HEADERS['User-Agent']}")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    svc = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=svc, options=opts)
    try:
        # Google トップに行き、検索ボックスに入力して送信（JS生成結果に対応）
        driver.get("https://www.google.com/")
        wait = WebDriverWait(driver, 8)
        try:
            # accept cookie 等があれば試しにクリック
            time.sleep(0.6)
            for b in driver.find_elements(By.TAG_NAME, "button"):
                txt = (b.text or "").strip()
                if txt and any(k in txt for k in ("同意", "I agree", "Accept", "同意する", "同意します")):
                    try:
                        b.click()
                        time.sleep(0.4)
                        break
                    except Exception:
                        pass
        except Exception:
            pass

        # 検索ボックスに入力して実行
        try:
            q = wait.until(lambda d: d.find_element(By.NAME, "q"))
            q.clear()
            q.send_keys(query)
            q.send_keys(Keys.ENTER)
        except Exception:
            # フォールバックで直接画像検索URLを開く
            driver.get(build_google_images_url(query))

        # 画像タブに切り替え（URLに tbm=isch を付ける場合もある）
        try:
            if "tbm=isch" not in driver.current_url:
                try:
                    img_tab = driver.find_element(By.CSS_SELECTOR, "a[href*='tbm=isch']")
                    img_tab.click()
                except Exception:
                    driver.get(build_google_images_url(query))
        except Exception:
            pass

        # 少しスクロールしてJSでlazy属性を解除・overlayを除去
        for _ in range(3):
            if deadline and time.time() > deadline:
                break
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight/3);")
            time.sleep(0.4)

        # DOM操作で lazy 属性を解除し、邪魔なオーバーレイを削除
        driver.execute_script("""
            try {
                document.querySelectorAll('img').forEach(function(img){
                    var s = img.getAttribute('data-iurl') || img.getAttribute('data-src') || (img.getAttribute('data-srcset')||'').split(' ')[0];
                    if(s && !img.src.includes(s)) {
                        try { img.src = s; } catch(e) {}
                    }
                    img.removeAttribute('srcset');
                    img.removeAttribute('loading');
                });
                document.querySelectorAll('[role=\"dialog\"],[aria-hidden=\"true\"], .S3Wjs, .mnr-c, .overlay, .kHssrc').forEach(function(e){ try{ e.remove(); }catch(e){} });
            } catch(e) {}
        """)

        # さらに数回スクロールしてサムネを読み込ませる
        for _ in range(4):
            if deadline and time.time() > deadline:
                break
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(0.4)

        found_urls = []
        seen = set()

        # 取得対象のサムネ要素を列挙（class 部分一致で絞る）
        thumbs = driver.find_elements(By.CSS_SELECTOR, f"img.{match_class_substr}") if match_class_substr else driver.find_elements(By.CSS_SELECTOR, "img")
        for thumb in thumbs:
            if deadline and time.time() > deadline:
                break
            # スクロール・クリックして大画像を表示
            try:
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", thumb)
                time.sleep(0.15)
                thumb.click()
            except Exception:
                # クリックできない要素は JS で src を取得する試行へ
                pass

            time.sleep(0.5)
            # JSで候補の src と natural size を取得（クリックで出る大画像を優先）
            srcs = driver.execute_script("""
                var out = [];
                var cand = document.querySelectorAll('img.n3VNCb, img[jsname], img.' + arguments[0]);
                cand.forEach(function(i){
                    try {
                        var s = i.getAttribute('src') || i.getAttribute('data-iurl') || i.getAttribute('data-src');
                        if(s && !s.startsWith('data:')) {
                            var w = i.naturalWidth || parseInt(i.getAttribute('width')) || 0;
                            var h = i.naturalHeight || parseInt(i.getAttribute('height')) || 0;
                            out.push([s, w, h]);
                        }
                    } catch(e){}
                });
                return out;
            """, match_class_substr)
            # srcs は [ [src, w, h], ... ]
            for entry in srcs:
                if deadline and time.time() > deadline:
                    break
                try:
                    src = entry[0]
                    w = int(entry[1]) if entry[1] is not None else 0
                    h = int(entry[2]) if entry[2] is not None else 0
                except Exception:
                    continue
                # サイズフィルタ：幅または高さが100未満なら除外
                if w < 100 or h < 100:
                    continue
                if not (src.startswith("http://") or src.startswith("https://")):
                    continue
                if src in seen:
                    continue
                seen.add(src)
                found_urls.append(src)
                if len(found_urls) >= max_count:
                    break
            if len(found_urls) >= max_count:
                break

        return found_urls
    finally:
        driver.quit()

def download_and_save(urls, out_dir, deadline=None):
    out_dir.mkdir(exist_ok=True)
    saved = 0
    for url in urls:
        # 全体の残り時間チェック
        if deadline and time.time() > deadline:
            print("タイムリミットに達したためダウンロードを中止します（途中まで保存しました）。")
            break
        remaining = (deadline - time.time()) if deadline else None
        # ダウンロードに割けるタイムアウトを残り時間に合わせて設定（最低1秒）
        to = 10
        if remaining is not None:
            if remaining <= 1:
                print("残り時間が不足しているためこれ以上のダウンロードは行いません。")
                break
            to = min(10, max(1, int(remaining) - 1))
        try:
            resp = requests.get(url, headers=HEADERS, stream=True, timeout=to)
            resp.raise_for_status()
        except Exception as e:
            print(f"ダウンロード失敗: {url} -> {e}")
            continue
        ctype = resp.headers.get("content-type", "")
        if not ctype.startswith("image/"):
            print(f"非画像 (content-type={ctype}): {url}")
            continue
        ext = mimetypes.guess_extension(ctype.split(";")[0]) or Path(url).suffix or ".jpg"
        if not ext.startswith("."):
            ext = "." + ext
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        fname = out_dir / f"{timestamp}_{saved+1}{ext}"
        counter = 1
        while fname.exists():
            fname = out_dir / f"{timestamp}_{saved+1}_{counter}{ext}"
            counter += 1
        try:
            with open(fname, "wb") as f:
                for chunk in resp.iter_content(8192):
                    # パーツ書き込み中に時間切れになってもファイルは部分的に残るが処理は中断しない
                    f.write(chunk)
            print(f"Saved: {fname.name}")
            saved += 1
        except Exception as e:
            print(f"保存失敗: {fname} -> {e}")
    return saved

def main():
    # ユーザ要求に合わせて入力は検索ワードのみ。クラスは固定 YQ4gaf、id は無視。
    query = input("検索ワードを入力してください (例: 大根): ").strip()
    if not query:
        print("検索ワードが空です。終了します。")
        return

    match_class = "YQ4gaf"   # 固定
    max_cnt = SAVE_MAX       # ユーザに枚数は聞かない（デフォルト7枚）

    start = time.time()
    deadline = start + MAX_RUNTIME

    print("ブラウザを起動して検索します。画面に表示して確認したい場合はブラウザを閉じないでください。")
    urls = collect_target_image_urls(query, match_id_substr=None, match_class_substr=match_class, max_count=max_cnt, headed=True, deadline=deadline)

    out_dir = Path(__file__).resolve().parent / "images"
    out_dir.mkdir(exist_ok=True)
    # srcs.txt に取得した URL を保存（デバッグ）
    with open(out_dir / "srcs.txt", "w", encoding="utf-8") as sf:
        for u in urls:
            sf.write(u + "\n")
    print(f"取得した URL を images/srcs.txt に保存（合計 {len(urls)} 件）")

    if not urls:
        print("条件に一致する画像が見つかりませんでした。class を確認してください。")
        return

    # 残り時間を考慮して可能な限りダウンロード（時間不足でも途中まで保存する）
    saved = download_and_save(urls, out_dir, deadline=deadline)

    print(f"完了: {saved} / {len(urls)} 保存")

if __name__ == "__main__":
    main()