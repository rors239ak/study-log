const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const message = document.getElementById("message");
const fireworkTypeSel = document.getElementById("fireworkType");
const colorPicker = document.getElementById("colorPicker");
const randomColorChk = document.getElementById("randomColor");
const fireworkSizeSel = document.getElementById("fireworkSize");
const undoBtn = document.getElementById("undoBtn");

let drawing = false;
let lastX = 0, lastY = 0;

// 履歴管理
let history = [];
function saveHistory() {
  history.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
  if (history.length > 30) history.shift();
}
function undo() {
  if (history.length > 0) {
    ctx.putImageData(history.pop(), 0, 0);
    message.textContent = "一個前に戻りました";
    setTimeout(() => message.textContent = "", 1000);
  }
}

// お絵描き（マウス・タッチ両対応）
function getPos(e) {
  const rect = canvas.getBoundingClientRect();
  let x, y;
  if (e.touches && e.touches.length > 0) {
    x = (e.touches[0].clientX - rect.left) * canvas.width / rect.width;
    y = (e.touches[0].clientY - rect.top) * canvas.height / rect.height;
  } else {
    x = (e.clientX - rect.left) * canvas.width / rect.width;
    y = (e.clientY - rect.top) * canvas.height / rect.height;
  }
  return [Math.round(x), Math.round(y)];
}

// お絵描き（マウス）
canvas.addEventListener("mousedown", e => {
  drawing = true;
  [lastX, lastY] = getPos(e);
  saveHistory();
});
canvas.addEventListener("mousemove", e => {
  if (!drawing) return;
  const [x, y] = getPos(e);
  ctx.strokeStyle = randomColor();
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(lastX, lastY);
  ctx.lineTo(x, y);
  ctx.stroke();
  [lastX, lastY] = [x, y];
});
canvas.addEventListener("mouseup", () => drawing = false);
canvas.addEventListener("mouseleave", () => drawing = false);

// お絵描き（タッチ）
canvas.addEventListener("touchstart", e => {
  drawing = true;
  [lastX, lastY] = getPos(e);
  saveHistory();
  e.preventDefault();
});
canvas.addEventListener("touchmove", e => {
  if (!drawing) return;
  const [x, y] = getPos(e);
  ctx.strokeStyle = randomColor();
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(lastX, lastY);
  ctx.lineTo(x, y);
  ctx.stroke();
  [lastX, lastY] = [x, y];
  e.preventDefault();
});
canvas.addEventListener("touchend", () => drawing = false);
canvas.addEventListener("touchcancel", () => drawing = false);

// 花火（マウス・タッチ両対応）
function handleFirework(x, y) {
  const type = fireworkTypeSel.value;
  let colorFunc;
  if (randomColorChk.checked) {
    colorFunc = randomColor;
  } else {
    const color = colorPicker.value;
    colorFunc = () => color;
  }
  const size = parseFloat(fireworkSizeSel.value);
  saveHistory();
  launchFirework(x, y, type, colorFunc, size);
  message.textContent = "花火が上がった！";
  setTimeout(() => message.textContent = "", 1200);
}

canvas.addEventListener("click", e => {
  const [x, y] = getPos(e);
  handleFirework(x, y);
});
canvas.addEventListener("touchend", e => {
  if (e.changedTouches && e.changedTouches.length > 0) {
    const rect = canvas.getBoundingClientRect();
    const x = (e.changedTouches[0].clientX - rect.left) * canvas.width / rect.width;
    const y = (e.changedTouches[0].clientY - rect.top) * canvas.height / rect.height;
    handleFirework(Math.round(x), Math.round(y));
    e.preventDefault();
  }
});

// 色選択の有効/無効
randomColorChk.addEventListener("change", () => {
  colorPicker.disabled = randomColorChk.checked;
});
colorPicker.disabled = randomColorChk.checked;

// ランダムカラー
function randomColor() {
  const h = Math.floor(Math.random() * 360);
  return `hsl(${h},90%,60%)`;
}

// 花火アニメーション
function launchFirework(x, y, type, colorFunc, size = 0.75) {
  let particles = [];
  let count = Math.round((40 + Math.random() * 16) * size);
  let radius = 15 * size; // 半径も半分
  switch (type) {
    case "normal":
      for (let i = 0; i < count; i++) {
        const angle = (2 * Math.PI * i) / count;
        const speed = (1 + Math.random() * 1) * size;
        particles.push({
          x, y,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed,
          color: colorFunc(),
          alpha: 1
        });
      }
      break;
    case "ring":
      for (let i = 0; i < count; i++) {
        const angle = (2 * Math.PI * i) / count;
        const speed = 1.5 * size;
        particles.push({
          x: x + Math.cos(angle) * radius,
          y: y + Math.sin(angle) * radius,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed,
          color: colorFunc(),
          alpha: 1
        });
      }
      break;
    case "star":
      for (let i = 0; i < count; i++) {
        const angle = (2 * Math.PI * i) / count;
        const speed = (1 + Math.random() * 1) * size;
        const star = Math.round(i % 5) === 0 ? 2 : 1;
        particles.push({
          x, y,
          vx: Math.cos(angle) * speed * star,
          vy: Math.sin(angle) * speed * star,
          color: colorFunc(),
          alpha: 1
        });
      }
      break;
    case "heart":
      for (let i = 0; i < count; i++) {
        const t = (2 * Math.PI * i) / count;
        const r = 6 * size * (1 - Math.sin(t));
        const speed = (1 + Math.random() * 0.75) * size;
        particles.push({
          x: x + r * Math.cos(t),
          y: y + r * Math.sin(t),
          vx: Math.cos(t) * speed,
          vy: Math.sin(t) * speed,
          color: colorFunc(),
          alpha: 1
        });
      }
      break;
    case "spiral":
      for (let i = 0; i < count; i++) {
        const angle = (2 * Math.PI * i) / count + i * 0.1;
        const speed = (1 + (i % 5) * 0.25) * size;
        particles.push({
          x, y,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed,
          color: colorFunc(),
          alpha: 1
        });
      }
      break;
    case "double":
      for (let i = 0; i < count; i++) {
        const angle = (2 * Math.PI * i) / count;
        const speed1 = (1 + Math.random() * 1) * size;
        const speed2 = (1.5 + Math.random() * 1) * size;
        particles.push({
          x, y,
          vx: Math.cos(angle) * speed1,
          vy: Math.sin(angle) * speed1,
          color: colorFunc(),
          alpha: 1
        });
        particles.push({
          x, y,
          vx: Math.cos(angle) * speed2,
          vy: Math.sin(angle) * speed2,
          color: colorFunc(),
          alpha: 1
        });
      }
      break;
    case "cross":
      for (let i = 0; i < count; i++) {
        const angle = (Math.PI / 2) * (i % 4);
        const speed = (1 + Math.random() * 1) * size;
        particles.push({
          x, y,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed,
          color: colorFunc(),
          alpha: 1
        });
      }
      break;
    case "random":
      const types = ["normal", "ring", "star", "heart", "spiral", "double", "cross"];
      const randType = types[Math.floor(Math.random() * types.length)];
      launchFirework(x, y, randType, colorFunc, size);
      return;
  }
  animateFirework(particles, 0, size);
}

function animateFirework(particles, frame, size = 0.75) {
  if (frame > 60) return;
  ctx.globalAlpha = 1;
  if (frame === 0) {
    ctx.beginPath();
    ctx.arc(particles[0].x, particles[0].y, 4 * size, 0, 2 * Math.PI);
    ctx.fillStyle = "#fff";
    ctx.globalAlpha = 0.7;
    ctx.fill();
  }
  ctx.globalAlpha = 1;
  for (const p of particles) {
    ctx.beginPath();
    ctx.arc(p.x, p.y, 2 * size, 0, 2 * Math.PI);
    ctx.fillStyle = p.color;
    ctx.globalAlpha = p.alpha;
    ctx.fill();
    p.x += p.vx;
    p.y += p.vy;
    p.vx *= 0.96;
    p.vy *= 0.96;
    p.alpha *= 0.96;
  }
  ctx.globalAlpha = 1;
  requestAnimationFrame(() => animateFirework(particles, frame + 1, size));
}

// スタンプ描画
function drawStamp(x, y, type) {
  ctx.save();
  ctx.font = "32px serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  switch (type) {
    case "audience":
      // 観客（顔の列）
      for (let i = -2; i <= 2; i++) {
        ctx.beginPath();
        ctx.arc(x + i * 18, y, 12, 0, 2 * Math.PI);
        ctx.fillStyle = "#fff";
        ctx.fill();
        ctx.strokeStyle = "#222";
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.fillStyle = "#222";
        ctx.beginPath();
        ctx.arc(x + i * 18 - 4, y - 2, 2, 0, 2 * Math.PI);
        ctx.arc(x + i * 18 + 4, y - 2, 2, 0, 2 * Math.PI);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(x + i * 18, y + 4, 4, 0, Math.PI);
        ctx.stroke();
      }
      break;
    case "river":
      // 川（青い波線）
      ctx.strokeStyle = "#33aaff";
      ctx.lineWidth = 6;
      ctx.beginPath();
      for (let i = 0; i <= 60; i += 6) {
        ctx.lineTo(x - 30 + i, y + Math.sin(i / 12) * 8);
      }
      ctx.stroke();
      break;
    case "star":
      ctx.fillStyle = "#ffe066";
      ctx.strokeStyle = "#ffb700";
      drawStar(ctx, x, y, 5, 16, 7);
      break;
    case "music":
      ctx.fillStyle = "#ffe066";
      ctx.fillText("♪", x, y + 2);
      break;
    case "clap":
      ctx.fillStyle = "#ffe066";
      ctx.fillText("👏", x, y + 2);
      break;
    case "smile":
      ctx.fillStyle = "#ffe066";
      ctx.fillText("😊", x, y + 2);
      break;
  }
  ctx.restore();
}

// 星型
function drawStar(ctx, cx, cy, spikes, outerRadius, innerRadius) {
  let rot = Math.PI / 2 * 3;
  let x = cx;
  let y = cy;
  let step = Math.PI / spikes;
  ctx.beginPath();
  ctx.moveTo(cx, cy - outerRadius);
  for (let i = 0; i < spikes; i++) {
    x = cx + Math.cos(rot) * outerRadius;
    y = cy + Math.sin(rot) * outerRadius;
    ctx.lineTo(x, y);
    rot += step;

    x = cx + Math.cos(rot) * innerRadius;
    y = cy + Math.sin(rot) * innerRadius;
    ctx.lineTo(x, y);
    rot += step;
  }
  ctx.lineTo(cx, cy - outerRadius);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
}