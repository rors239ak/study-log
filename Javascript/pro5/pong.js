const canvas = document.getElementById('pong');
const ctx = canvas.getContext('2d');

const PADDLE_WIDTH = 15, PADDLE_HEIGHT = 100, PADDLE_SPEED = 6;
const BALL_SIZE = 16, BALL_SPEED = 6;
const WINNING_SCORE = 5;

let leftPaddle = {
    x: 10,
    y: canvas.height/2 - PADDLE_HEIGHT/2,
    width: PADDLE_WIDTH,
    height: PADDLE_HEIGHT,
    dy: 0
};

let rightPaddle = {
    x: canvas.width - PADDLE_WIDTH - 10,
    y: canvas.height/2 - PADDLE_HEIGHT/2,
    width: PADDLE_WIDTH,
    height: PADDLE_HEIGHT,
    dy: 0
};

let ball = {
    x: canvas.width/2 - BALL_SIZE/2,
    y: canvas.height/2 - BALL_SIZE/2,
    size: BALL_SIZE,
    dx: BALL_SPEED * (Math.random() > 0.5 ? 1 : -1),
    dy: BALL_SPEED * (Math.random() > 0.5 ? 1 : -1)
};

let score = { left: 0, right: 0 };
let upPressed = false, downPressed = false;
let gameOver = false;

function drawRect(x, y, w, h, color="#fff") {
    ctx.fillStyle = color;
    ctx.fillRect(x, y, w, h);
}

function drawBall() {
    ctx.fillStyle = "#0ff";
    ctx.fillRect(ball.x, ball.y, ball.size, ball.size);
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Middle dashed line
    ctx.strokeStyle = "#888";
    ctx.setLineDash([10, 10]);
    ctx.beginPath();
    ctx.moveTo(canvas.width/2, 0);
    ctx.lineTo(canvas.width/2, canvas.height);
    ctx.stroke();
    ctx.setLineDash([]);

    drawRect(leftPaddle.x, leftPaddle.y, leftPaddle.width, leftPaddle.height);
    drawRect(rightPaddle.x, rightPaddle.y, rightPaddle.width, rightPaddle.height);
    drawBall();
}

function movePaddles() {
    // Mouse and keyboard for left paddle
    if (upPressed) leftPaddle.y -= PADDLE_SPEED;
    if (downPressed) leftPaddle.y += PADDLE_SPEED;

    // Clamp to canvas
    leftPaddle.y = Math.max(0, Math.min(canvas.height - leftPaddle.height, leftPaddle.y));

    // Computer paddle AI: follow ball with smoothing
    let target = ball.y + ball.size/2 - rightPaddle.height/2;
    let aiSpeed = Math.min(PADDLE_SPEED, Math.abs(target - rightPaddle.y));
    if (target > rightPaddle.y) rightPaddle.y += aiSpeed;
    else if (target < rightPaddle.y) rightPaddle.y -= aiSpeed;
    rightPaddle.y = Math.max(0, Math.min(canvas.height - rightPaddle.height, rightPaddle.y));
}

function moveBall() {
    ball.x += ball.dx;
    ball.y += ball.dy;

    // Top/bottom wall collision
    if (ball.y < 0 || ball.y + ball.size > canvas.height) {
        ball.dy *= -1;
        ball.y = Math.max(0, Math.min(canvas.height - ball.size, ball.y));
    }

    // Paddle collision
    if (ball.x < leftPaddle.x + leftPaddle.width &&
        ball.y + ball.size > leftPaddle.y &&
        ball.y < leftPaddle.y + leftPaddle.height) {
        ball.dx *= -1;
        ball.x = leftPaddle.x + leftPaddle.width;
        // Add a bit of "spin"
        let centerDiff = (ball.y + ball.size/2) - (leftPaddle.y + leftPaddle.height/2);
        ball.dy += centerDiff * 0.25 / (PADDLE_HEIGHT/2);
    }

    if (ball.x + ball.size > rightPaddle.x &&
        ball.y + ball.size > rightPaddle.y &&
        ball.y < rightPaddle.y + rightPaddle.height) {
        ball.dx *= -1;
        ball.x = rightPaddle.x - ball.size;
        let centerDiff = (ball.y + ball.size/2) - (rightPaddle.y + rightPaddle.height/2);
        ball.dy += centerDiff * 0.25 / (PADDLE_HEIGHT/2);
    }

    // Score
    if (ball.x < 0) {
        score.right++;
        updateScore();
        resetBall();
    } else if (ball.x + ball.size > canvas.width) {
        score.left++;
        updateScore();
        resetBall();
    }
}

function updateScore() {
    document.getElementById('score-left').textContent = score.left;
    document.getElementById('score-right').textContent = score.right;
    if (score.left >= WINNING_SCORE || score.right >= WINNING_SCORE) {
        gameOver = true;
        setTimeout(() => alert(`${score.left >= WINNING_SCORE ? "You" : "Computer"} win!`), 100);
    }
}

function resetBall() {
    ball.x = canvas.width/2 - BALL_SIZE/2;
    ball.y = canvas.height/2 - BALL_SIZE/2;
    // Randomize ball direction
    ball.dx = BALL_SPEED * (Math.random() > 0.5 ? 1 : -1);
    ball.dy = BALL_SPEED * (Math.random()*2 - 1);
}

function gameLoop() {
    if (!gameOver) {
        movePaddles();
        moveBall();
        draw();
        requestAnimationFrame(gameLoop);
    }
}

// Keyboard controls
document.addEventListener('keydown', e => {
    if (e.key === "ArrowUp") upPressed = true;
    if (e.key === "ArrowDown") downPressed = true;
});
document.addEventListener('keyup', e => {
    if (e.key === "ArrowUp") upPressed = false;
    if (e.key === "ArrowDown") downPressed = false;
});

// Mouse controls for left paddle
canvas.addEventListener('mousemove', e => {
    const rect = canvas.getBoundingClientRect();
    const mouseY = e.clientY - rect.top;
    leftPaddle.y = mouseY - leftPaddle.height/2;
    leftPaddle.y = Math.max(0, Math.min(canvas.height - leftPaddle.height, leftPaddle.y));
});

draw();
gameLoop();