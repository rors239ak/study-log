<?php
session_start();

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
    <h1>1問目</h1>
    <p>新郎と新婦の初めてのデート先はどこでしょう？</p>
    <form action="check1.php" method="post">
      <input type="radio" name="question1" value="映画館">映画館<br>
      <input type="radio" name="question1" value="ボードゲームカフェ">ボードゲームカフェ<br>
      <input type="radio" name="question1" value="海">海<br>
      <input type="radio" name="question1" value="油山の夜景">油山の夜景<br>
      <input type="submit" value="次へ">
    </form>
    <p><a href="index.php">最初に戻る</a></p>
  </main>
  </main>

  <footer>
    <a href="question2.php"><img src="" alt=""></a> <!-- ロゴとホームへ戻るリンク -->
  </footer>
</body>
</html>