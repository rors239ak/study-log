<?php
session_start();
// 直アクセス防止：question4が未回答なら戻す
if (!isset($_SESSION['question4'])) {
  header('Location: question4.php');
  exit;
}
?>
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>新郎・新婦検定</title>
</head>
<body>  
  <header>
    <a href=""><img src="" alt=""></a> <!-- ロゴとホームへ戻るリンク -->
  </header>

  <main>
    <h1>5問目</h1>
    <p>新婦の好きな花は？
    </p>
    <form action="check5.php" method="post">
      <input type="radio" name="question5" value="バラ">バラ<br>
      <input type="radio" name="question5" value="朝顔">朝顔<br>
      <input type="radio" name="question5" value="ゆり">ゆり<br>
      <input type="radio" name="question5" value="ひまわり">ひまわり<br>

      <p class="last_check">これで問題は以上となります。<br>
        答えのボタンを押すとすぐに点数が出ます。</p>
      <input type="submit" value="答え">
    </form>
    <p><a href="index.php">最初に戻る</a></p>
  </main>
  </main>

  <footer>
    <a href=""><img src="" alt=""></a> <!-- ロゴとホームへ戻るリンク -->
  </footer>
</body>
</html>