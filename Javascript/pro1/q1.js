const board = document.getElementById("board");
const message = document.getElementById("message");
const resetBtn = document.getElementById("reset");
const levelSel = document.getElementById("levelSel");
const expbar = document.getElementById("expbar");
const expfill = document.getElementById("expfill");
const levelinfo = document.getElementById("levelinfo");

let cells, turn, gameOver, human, ai, aiLevel;
let playerLevel = 1;
let playerExp = 0;
let nextExp = 10;

function saveStatus() {
  localStorage.setItem("ttt_level", playerLevel);
  localStorage.setItem("ttt_exp", playerExp);
}
function loadStatus() {
  playerLevel = parseInt(localStorage.getItem("ttt_level")) || 1;
  playerExp = parseInt(localStorage.getItem("ttt_exp")) || 0;
  nextExp = 10 + (playerLevel - 1) * 5;
}
function updateExpBar() {
  levelinfo.textContent = `レベル: ${playerLevel}　経験値: ${playerExp} / ${nextExp}`;
  expfill.style.width = Math.min(100, playerExp / nextExp * 100) + "%";
}
function addExp(amount) {
  playerExp += amount;
  while (playerExp >= nextExp) {
    playerExp -= nextExp;
    playerLevel++;
    nextExp = 10 + (playerLevel - 1) * 5;
    message.textContent += ` レベルアップ！`;
  }
  updateExpBar();
  saveStatus();
}

function initGame() {
  cells = Array(9).fill("");
  turn = "〇"; // 人間が先手
  human = "〇";
  ai = "✕";
  aiLevel = levelSel.value;
  gameOver = false;
  message.textContent = "あなたは〇です。あなたの番です";
  drawBoard();
  updateExpBar();
}

function drawBoard(winLine = []) {
  board.innerHTML = "";
  cells.forEach((cell, i) => {
    const div = document.createElement("div");
    div.className = "cell";
    if (winLine.includes(i)) div.classList.add("win");
    div.textContent = cell;
    div.addEventListener("click", () => handleClick(i));
    board.appendChild(div);
  });
}

function handleClick(i) {
  if (cells[i] !== "" || gameOver || turn !== human) return;
  cells[i] = human;
  const winLine = checkWin(human);
  drawBoard(winLine);
  if (winLine.length > 0) {
    message.textContent = "あなたの勝ち！ +5EXP";
    addExp(5);
    gameOver = true;
    return;
  } else if (cells.every(cell => cell !== "")) {
    message.textContent = "引き分け！ +2EXP";
    addExp(2);
    gameOver = true;
    return;
  }
  turn = ai;
  message.textContent = "AIの番です";
  setTimeout(aiMove, 400);
}

function aiMove() {
  let move;
  if (aiLevel === "easy") {
    move = randomMove();
  } else if (aiLevel === "normal") {
    move = normalMove();
  } else if (aiLevel === "hard") {
    move = minimaxRoot();
  }
  if (move !== undefined) {
    cells[move] = ai;
  }
  const winLine = checkWin(ai);
  drawBoard(winLine);
  if (winLine.length > 0) {
    message.textContent = "AIの勝ち！ +1EXP";
    addExp(1);
    gameOver = true;
    return;
  } else if (cells.every(cell => cell !== "")) {
    message.textContent = "引き分け！ +2EXP";
    addExp(2);
    gameOver = true;
    return;
  }
  turn = human;
  message.textContent = "あなたの番です";
}

// ランダム
function randomMove() {
  const empty = cells.map((v, i) => v === "" ? i : null).filter(i => i !== null);
  return empty[Math.floor(Math.random() * empty.length)];
}

// 普通：勝てるときは勝つ、防ぐ、それ以外はランダム
function normalMove() {
  let move = findWinningMove(ai);
  if (move !== undefined) return move;
  move = findWinningMove(human);
  if (move !== undefined) return move;
  return randomMove();
}

// ミニマックス法（最強AI）
function minimaxRoot() {
  let bestScore = -Infinity;
  let bestMove = null;
  for (let i = 0; i < 9; i++) {
    if (cells[i] === "") {
      cells[i] = ai;
      let score = minimax(cells, 0, false);
      cells[i] = "";
      if (score > bestScore) {
        bestScore = score;
        bestMove = i;
      }
    }
  }
  return bestMove;
}
function minimax(newCells, depth, isMax) {
  const winner = getWinner(newCells);
  if (winner === ai) return 10 - depth;
  if (winner === human) return depth - 10;
  if (newCells.every(cell => cell !== "")) return 0;

  if (isMax) {
    let best = -Infinity;
    for (let i = 0; i < 9; i++) {
      if (newCells[i] === "") {
        newCells[i] = ai;
        best = Math.max(best, minimax(newCells, depth + 1, false));
        newCells[i] = "";
      }
    }
    return best;
  } else {
    let best = Infinity;
    for (let i = 0; i < 9; i++) {
      if (newCells[i] === "") {
        newCells[i] = human;
        best = Math.min(best, minimax(newCells, depth + 1, true));
        newCells[i] = "";
      }
    }
    return best;
  }
}

function getWinner(cellsArr) {
  const wins = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
  ];
  for (const line of wins) {
    const [a, b, c] = line;
    if (cellsArr[a] && cellsArr[a] === cellsArr[b] && cellsArr[a] === cellsArr[c]) {
      return cellsArr[a];
    }
  }
  return null;
}

function checkWin(player) {
  const wins = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
  ];
  return wins.find(line => line.every(idx => cells[idx] === player)) || [];
}

function findWinningMove(who) {
  for (let i = 0; i < 9; i++) {
    if (cells[i] !== "") continue;
    cells[i] = who;
    if (checkWin(who).length > 0) {
      cells[i] = "";
      return i;
    }
    cells[i] = "";
  }
  return undefined;
}

resetBtn.addEventListener("click", initGame);
levelSel.addEventListener("change", initGame);

loadStatus();
initGame();
