<?php 
session_start();
$_SESSION["question_count"] = 0; ?>
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="style.css">
  <title>新郎・新婦検定</title>
</head>
<body>  
  <header>
    <a href=""><img src="" alt=""></a> <!-- ロゴとホームへ戻るリンク -->
  </header>

  <main>
    <h1>新郎・新婦検定</h1>
    <form action="start.php" method="post">
      <label>名前
      <input type="text" class="textbox" name="name">
      <p>下の【スタート】を押すと問題が4択で表示されますので、できるだけ早くお答えください。<br>なお、【スタート】を押してから【終了】を押すまでの時間が計測されていますのでそれによって点数も変わってきます。</p> 
      <p>それでは準備はいいですか？</p>
      <button class="btn" type="submit">スタート</button>
    </form></label>
  </main>

  <footer>
    <a href=""><img src="" alt=""></a> <!-- ロゴとホームへ戻るリンク -->
  </footer>
</body>
</html>