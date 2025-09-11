const SIZE = 10;
const WIN_COUNT = 5;

const board = document.getElementById("board");
const message = document.getElementById("message");
const resetBtn = document.getElementById("reset");
const levelSel = document.getElementById("level");
const startBtn = document.getElementById("start");

let cells, turn, gameOver, level, player, computer;

function showBoard(show) {
  board.style.display = show ? "" : "none";
  resetBtn.style.display = show ? "" : "none";
}

function initGame() {
  cells = Array(SIZE * SIZE).fill("");
  turn = "black";
  gameOver = false;
  player = "black";
  computer = "white";
  message.textContent = "あなたは「黒石（●）」！ あなたの番です";
  drawBoard();
  showBoard(true);
  if (level === "settai") {
    message.textContent += "（せったいモード）";
  }
}

function drawBoard(winLine = []) {
  board.innerHTML = "";
  for (let i = 0; i < SIZE * SIZE; i++) {
    const div = document.createElement("div");
    div.className = "cell";
    if (winLine.includes(i)) div.classList.add("win");
    if (cells[i] === "black") {
      const stone = document.createElement("div");
      stone.className = "stone-black";
      div.appendChild(stone);
    } else if (cells[i] === "white") {
      const stone = document.createElement("div");
      stone.className = "stone-white";
      div.appendChild(stone);
    }
    div.addEventListener("click", () => handleClick(i));
    board.appendChild(div);
  }
}

function handleClick(i) {
  if (cells[i] !== "" || gameOver || turn !== player) return;
  cells[i] = player;
  const winLine = checkWin(player);
  drawBoard(winLine);
  if (winLine.length > 0) {
    message.textContent = "おめでとう！あなたの勝ち！";
    gameOver = true;
    return;
  } else if (cells.every(cell => cell !== "")) {
    message.textContent = "引き分け！";
    gameOver = true;
    return;
  }
  turn = computer;
  message.textContent = "コンピューターの番です";
  setTimeout(computerMove, 400);
}

function computerMove() {
  let move;
  if (level === "easy") {
    move = randomMove();
  } else if (level === "normal") {
    move = normalMove();
  } else if (level === "hard") {
    move = minimaxRoot(3, computer); // 3手先まで読む
  } else if (level === "settai") {
    move = settaiMove();
  }
  if (move !== undefined) {
    cells[move] = computer;
  }
  const winLine = checkWin(computer);
  drawBoard(winLine);
  if (winLine.length > 0) {
    message.textContent = "コンピューターの勝ち！";
    gameOver = true;
    return;
  } else if (cells.every(cell => cell !== "")) {
    message.textContent = "引き分け！";
    gameOver = true;
    return;
  }
  turn = player;
  message.textContent = "あなたの番です";
}

// ランダムな空きマス
function randomMove() {
  const empty = cells.map((v, i) => v === "" ? i : null).filter(i => i !== null);
  return empty[Math.floor(Math.random() * empty.length)];
}

// 普通：勝てるときは勝つ、負けそうなら防ぐ、それ以外はランダム
function normalMove() {
  let move = findWinningMove(computer);
  if (move !== undefined) return move;
  move = findWinningMove(player);
  if (move !== undefined) return move;
  return randomMove();
}

// 難しい：ミニマックス法（3手先まで読む）
function minimaxRoot(depth, who) {
  let bestScore = -Infinity;
  let bestMove = null;
  const empty = cells.map((v, i) => v === "" ? i : null).filter(i => i !== null);
  for (let i of empty) {
    cells[i] = who;
    let score = minimax(depth - 1, false, who, player, -Infinity, Infinity);
    cells[i] = "";
    if (score > bestScore) {
      bestScore = score;
      bestMove = i;
    }
  }
  return bestMove;
}
function minimax(depth, isMax, ai, human, alpha, beta) {
  const aiWin = checkWin(ai);
  const humanWin = checkWin(human);
  if (aiWin.length > 0) return 10000 + depth;
  if (humanWin.length > 0) return -10000 - depth;
  if (cells.every(cell => cell !== "") || depth === 0) return evaluateBoard(ai) - evaluateBoard(human);

  const empty = cells.map((v, i) => v === "" ? i : null).filter(i => i !== null);
  if (isMax) {
    let maxEval = -Infinity;
    for (let i of empty) {
      cells[i] = ai;
      let evalScore = minimax(depth - 1, false, ai, human, alpha, beta);
      cells[i] = "";
      maxEval = Math.max(maxEval, evalScore);
      alpha = Math.max(alpha, evalScore);
      if (beta <= alpha) break;
    }
    return maxEval;
  } else {
    let minEval = Infinity;
    for (let i of empty) {
      cells[i] = human;
      let evalScore = minimax(depth - 1, true, ai, human, alpha, beta);
      cells[i] = "";
      minEval = Math.min(minEval, evalScore);
      beta = Math.min(beta, evalScore);
      if (beta <= alpha) break;
    }
    return minEval;
  }
}

// 接待：絶対に勝たせる
function settaiMove() {
  let move = findWinningMove(player);
  if (move !== undefined) {
    const empty = cells.map((v, i) => v === "" ? i : null).filter(i => i !== null);
    const others = empty.filter(i => i !== move);
    if (others.length > 0) return others[Math.floor(Math.random() * others.length)];
    return move;
  }
  let win = findWinningMove(computer);
  if (win !== undefined) {
    const empty = cells.map((v, i) => v === "" ? i : null).filter(i => i !== null);
    const others = empty.filter(i => i !== win);
    if (others.length > 0) return others[Math.floor(Math.random() * others.length)];
    return win;
  }
  return randomMove();
}

// 5つ並びを探す
function checkWin(player) {
  for (let y = 0; y < SIZE; y++) {
    for (let x = 0; x < SIZE; x++) {
      // 横
      if (x <= SIZE - WIN_COUNT) {
        let line = [];
        for (let k = 0; k < WIN_COUNT; k++) {
          if (cells[y * SIZE + x + k] === player) {
            line.push(y * SIZE + x + k);
          }
        }
        if (line.length === WIN_COUNT) return line;
      }
      // 縦
      if (y <= SIZE - WIN_COUNT) {
        let line = [];
        for (let k = 0; k < WIN_COUNT; k++) {
          if (cells[(y + k) * SIZE + x] === player) {
            line.push((y + k) * SIZE + x);
          }
        }
        if (line.length === WIN_COUNT) return line;
      }
      // 斜め（右下）
      if (x <= SIZE - WIN_COUNT && y <= SIZE - WIN_COUNT) {
        let line = [];
        for (let k = 0; k < WIN_COUNT; k++) {
          if (cells[(y + k) * SIZE + (x + k)] === player) {
            line.push((y + k) * SIZE + (x + k));
          }
        }
        if (line.length === WIN_COUNT) return line;
      }
      // 斜め（左下）
      if (x >= WIN_COUNT - 1 && y <= SIZE - WIN_COUNT) {
        let line = [];
        for (let k = 0; k < WIN_COUNT; k++) {
          if (cells[(y + k) * SIZE + (x - k)] === player) {
            line.push((y + k) * SIZE + (x - k));
          }
        }
        if (line.length === WIN_COUNT) return line;
      }
    }
  }
  return [];
}

// 勝てる手を探す
function findWinningMove(who) {
  for (let i = 0; i < SIZE * SIZE; i++) {
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

// 簡易評価関数
function evaluateBoard(who) {
  let max = 0;
  for (let y = 0; y < SIZE; y++) {
    for (let x = 0; x < SIZE; x++) {
      // 横
      if (x <= SIZE - WIN_COUNT) {
        let count = 0;
        for (let k = 0; k < WIN_COUNT; k++) {
          if (cells[y * SIZE + x + k] === who) count++;
        }
        if (count > max) max = count;
      }
      // 縦
      if (y <= SIZE - WIN_COUNT) {
        let count = 0;
        for (let k = 0; k < WIN_COUNT; k++) {
          if (cells[(y + k) * SIZE + x] === who) count++;
        }
        if (count > max) max = count;
      }
      // 斜め（右下）
      if (x <= SIZE - WIN_COUNT && y <= SIZE - WIN_COUNT) {
        let count = 0;
        for (let k = 0; k < WIN_COUNT; k++) {
          if (cells[(y + k) * SIZE + (x + k)] === who) count++;
        }
        if (count > max) max = count;
      }
      // 斜め（左下）
      if (x >= WIN_COUNT - 1 && y <= SIZE - WIN_COUNT) {
        let count = 0;
        for (let k = 0; k < WIN_COUNT; k++) {
          if (cells[(y + k) * SIZE + (x - k)] === who) count++;
        }
        if (count > max) max = count;
      }
    }
  }
  return max;
}

// イベント
resetBtn.addEventListener("click", () => {
  showBoard(false);
  message.textContent = "";
});
startBtn.addEventListener("click", () => {
  level = levelSel.value;
  initGame();
});

// 初期状態
showBoard(false);
message.textContent = "スタートボタンを押してね！";
