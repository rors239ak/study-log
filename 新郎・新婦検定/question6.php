<?php
session_start();
// 直アクセス防止：question5が未回答なら戻す
if (!isset($_SESSION['question5'])) {
  header('Location: question5.php');
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
    <h1>6問目</h1>
    <p>新郎の好きな新婦のご飯は？
    </p>
    <form action="check6.php" method="post">
      <input type="radio" name="question6" value="春巻き">春巻き<br>
      <input type="radio" name="question6" value="肉じゃが">肉じゃが<br>
      <input type="radio" name="question6" value="オムライス">オムライス<br>
      <input type="radio" name="question6" value="カルボナーラ">カルボナーラ<br>
      <input type="submit" value="次へ">
    </form>
    <p><a href="index.php">最初に戻る</a></p>
  </main>
  </main>

  <footer>
    <a href=""><img src="" alt=""></a> <!-- ロゴとホームへ戻るリンク -->
  </footer>
</body>
</html>