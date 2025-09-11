const canvas = document.getElementById("tetris");
const ctx = canvas.getContext("2d");
const scoreEl = document.getElementById("score");
const levelEl = document.getElementById("level");
const startBtn = document.getElementById("startBtn");
const message = document.getElementById("message");

const COLS = 10, ROWS = 20, BLOCK = 20;
canvas.width = COLS * BLOCK;
canvas.height = ROWS * BLOCK;

const COLORS = [
  null,
  "#00f0f0", // I
  "#0000f0", // J
  "#f0a000", // L
  "#f0f000", // O
  "#00f000", // S
  "#a000f0", // T
  "#f00000"  // Z
];

const SHAPES = [
  [],
  [[0,1],[1,1],[2,1],[3,1]], // I
  [[0,0],[0,1],[1,1],[2,1]], // J
  [[2,0],[0,1],[1,1],[2,1]], // L
  [[1,0],[2,0],[1,1],[2,1]], // O
  [[1,0],[2,0],[0,1],[1,1]], // S
  [[1,0],[0,1],[1,1],[2,1]], // T
  [[0,0],[1,0],[1,1],[2,1]]  // Z
];

let board, current, next, score, level, dropInterval, dropTimer, isGameOver;

function resetGame() {
  board = Array.from({length: ROWS}, () => Array(COLS).fill(0));
  score = 0;
  level = 1;
  isGameOver = false;
  updateScore();
  updateLevel();
  spawn();
  if (dropTimer) clearInterval(dropTimer);
  dropInterval = 700;
  dropTimer = setInterval(drop, dropInterval);
  message.textContent = "";
  draw();
}

function updateScore() {
  scoreEl.textContent = score;
}
function updateLevel() {
  levelEl.textContent = level;
}

function spawn() {
  const id = Math.floor(Math.random() * 7) + 1;
  current = {
    id,
    shape: SHAPES[id].map(([x, y]) => [x, y]),
    x: 3,
    y: 0
  };
  if (!valid(current.shape, current.x, current.y)) {
    isGameOver = true;
    message.textContent = "ゲームオーバー！";
    clearInterval(dropTimer);
  }
}

function drawBlock(x, y, colorId, alpha = 1) {
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.fillStyle = COLORS[colorId];
  ctx.fillRect(x * BLOCK, y * BLOCK, BLOCK - 1, BLOCK - 1);
  ctx.strokeStyle = "#222";
  ctx.strokeRect(x * BLOCK, y * BLOCK, BLOCK, BLOCK);
  ctx.restore();
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // board
  for (let y = 0; y < ROWS; y++) {
    for (let x = 0; x < COLS; x++) {
      if (board[y][x]) drawBlock(x, y, board[y][x]);
    }
  }
  // ゴースト（半透明）
  if (current) {
    const ghostY = getGhostY();
    for (const [dx, dy] of current.shape) {
      drawBlock(current.x + dx, ghostY + dy, current.id, 0.3);
    }
  }
  // current
  if (current) {
    for (const [dx, dy] of current.shape) {
      drawBlock(current.x + dx, current.y + dy, current.id, 1);
    }
  }
}

function valid(shape, x, y) {
  return shape.every(([dx, dy]) => {
    const nx = x + dx, ny = y + dy;
    return nx >= 0 && nx < COLS && ny >= 0 && ny < ROWS && (!board[ny] || !board[ny][nx]);
  });
}

function merge() {
  for (const [dx, dy] of current.shape) {
    const nx = current.x + dx, ny = current.y + dy;
    if (ny >= 0 && ny < ROWS && nx >= 0 && nx < COLS) {
      board[ny][nx] = current.id;
    }
  }
}

function rotate(shape) {
  // 中心(1,1)で回転
  return shape.map(([x, y]) => [y, -x]);
}

function hardDrop() {
  while (move(0, 1)) {}
  drop();
}

function move(dx, dy) {
  const nx = current.x + dx, ny = current.y + dy;
  if (valid(current.shape, nx, ny)) {
    current.x = nx;
    current.y = ny;
    draw();
    return true;
  }
  return false;
}

function rotateCurrent() {
  const newShape = current.shape.map(([x, y]) => [y, -x]);
  if (valid(newShape, current.x, current.y)) {
    current.shape = newShape;
    draw();
  }
}

function drop() {
  if (isGameOver) return;
  if (move(0, 1)) return;
  merge();
  clearLines();
  spawn();
  draw();
}

function clearLines() {
  let lines = 0;
  for (let y = ROWS - 1; y >= 0; y--) {
    if (board[y].every(v => v)) {
      board.splice(y, 1);
      board.unshift(Array(COLS).fill(0));
      lines++;
      y++;
    }
  }
  if (lines > 0) {
    score += [0, 40, 100, 300, 1200][lines] * level;
    updateScore();
    if (score >= level * 500) {
      level++;
      updateLevel();
      dropInterval = Math.max(100, 700 - (level - 1) * 60);
      clearInterval(dropTimer);
      dropTimer = setInterval(drop, dropInterval);
    }
  }
}

// ゴースト（落下位置予測）Y座標を返す
function getGhostY() {
  let ghostY = current.y;
  while (valid(current.shape, current.x, ghostY + 1)) {
    ghostY++;
  }
  return ghostY;
}

document.addEventListener("keydown", e => {
  if (isGameOver) return;
  switch (e.key) {
    case "ArrowLeft":
      move(-1, 0);
      break;
    case "ArrowRight":
      move(1, 0);
      break;
    case "ArrowDown":
      move(0, 1);
      break;
    case " ":
      e.preventDefault(); // スクロール防止
      rotateCurrent();
      break;
  }
});

startBtn.addEventListener("click", resetGame);

resetGame();