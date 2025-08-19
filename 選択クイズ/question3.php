<?php
session_start();
// 直アクセス防止：question2が未回答なら戻す
if (!isset($_SESSION['question2'])) {
  header('Location: question2.php');
  exit;
}
?>
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>選択クイズ</title>
</head>
<body>  
  <header>
    <a href=""><img src="" alt=""></a> <!-- ロゴとホームへ戻るリンク -->
  </header>

  <main>
    <h1>3問目</h1>
    <p>新婦と新婦の喧嘩の時に新婦が最初にとる行動は？
    </p>
    <form action="check3.php" method="post">
      <input type="radio" name="question3" value="謝罪">謝罪<br>
      <input type="radio" name="question3" value="家出">家出<br>
      <input type="radio" name="question3" value="無視">無視<br>
      <input type="radio" name="question3" value="爆買い">爆買い<br>
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