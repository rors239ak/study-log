<?php
session_start();
// 直アクセス防止：question3が未回答なら戻す
if (!isset($_SESSION['question3'])) {
  header('Location: question3.php');
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
    <h1>4問目</h1>
    <p>平野家でのみ流行っている口癖は？
    </p>
    <form action="check4.php" method="post">
      <input type="radio" name="question4" value="～しん">～しん<br>
      <input type="radio" name="question4" value="ニキ・ネキ">ニキ・ネキ<br>
      <input type="radio" name="question4" value="にゃんちゅう">にゃんちゅう<br>
      <input type="radio" name="question4" value="なんちゃって">なんちゃって<br>
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