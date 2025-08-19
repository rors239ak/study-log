<?php
session_start();


if (!isset($_POST['question3'])) {
  header('Location: question3.php');
  exit;
}

// セッションに保存
$_SESSION['question3'] = $_POST['question3'];

// 次のページへ
header('Location: question4.php');
exit;
