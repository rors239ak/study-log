<?php
session_start();
// 直アクセス防止：question1が未回答なら戻す
if (!isset($_SESSION['question1'])) {
  header('Location: question1.php');
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
    <h1>2問目</h1>
    <p>新郎が一番好きな新婦のチャームポイントは？
    </p>
    <form action="check2.php" method="post">
      <input type="radio" name="question2" value="髪質">髪質<br>
      <input type="radio" name="question2" value="目">目<br>
      <input type="radio" name="question2" value="歯">歯<br>
      <input type="radio" name="question2" value="脚">脚<br>
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