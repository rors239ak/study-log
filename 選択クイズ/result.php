<?php
// ← 先頭に空白や改行ナシ！
if (session_status() === PHP_SESSION_NONE) session_start();

if (!isset($_SESSION['start_time'])) {
  header('Location: check4.php'); exit;
}

// 【仮】終了時刻いまこの瞬間（本番は end.php から渡す）
$end = microtime(true);
$elapsed = $end - $_SESSION['start_time'];

// mm:ss.mmm に整形
$min = (int)floor($elapsed / 60);
$sec = $elapsed - ($min * 60);
$disp = sprintf('%02d:%06.3f', $min, $sec);

// 次のためにクリア（連打で壊れないように）
unset($_SESSION['start_time']);




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
    <table border="1">
  <tr>
    <th>問題</th>
    <th><?php echo $_SESSION["name"] ?>さんの回答</th>
    <th>結果</th>
    <th>正解は…</th>
  </tr>
  <tr>
    <td>質問1</td>
    <td><?php echo $_SESSION["question1"]; ?></td>
  </tr>
  <tr>
    <td>質問2</td>
    <td><?php echo $_SESSION["question2"]; ?></td>
  </tr>
  <tr>
    <td>質問3</td>
    <td><?php echo $_SESSION["question3"]; ?></td>
  </tr>
  <tr>
    <td>質問4</td>
    <td><?php echo $_SESSION["question4"]; ?></td>
  </tr>
</table>

    <p>かかった時間：<?= htmlspecialchars($disp, ENT_QUOTES, 'UTF-8') ?></p>
  <p><a href="index.php">最初に戻る</a></p>
  </main>

  <footer>
    <a href=""><img src="" alt=""></a> <!-- ロゴとホームへ戻るリンク -->
  </footer>
</body>
</html>