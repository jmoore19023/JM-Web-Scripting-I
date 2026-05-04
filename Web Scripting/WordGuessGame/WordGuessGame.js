/* ============================================================
   word-game.js
   Structure:
     WORDS          – word list
     GameLogic      – pure state, no DOM
     UI             – all DOM reads/writes
     Init           – wires everything together
   ============================================================ */


/* ── WORDS ─────────────────────────────────────────────────── */

const WORDS = [
  "APPLE", "BRAVE", "CHESS", "CROWD", "DWARF",
  "EARLY", "FLAME", "GHOST", "HAPPY", "IVORY",
  "JOKER", "KNEEL", "LASER", "MONKS", "NOBLE",
  "OCEAN", "PIANO", "QUEEN", "RIVAL", "SHEEP",
  "TIGER", "ULTRA", "VIVID", "WITCH", "XENON",
  "YACHT", "ZEBRA", "BLOOM", "CRISP", "DELVE",
  "EMBER", "FOUND", "GRAZE", "HONEY", "INPUT",
  "JUICE", "KITTY", "LEMON", "MOUTH", "NERVE",
  "OPERA", "PLUMB", "QUART", "ROUND", "SOLAR",
  "THUMB", "UNIFY", "VIOLA", "WATER", "EXACT"
];

function pickRandomWord() {
  return WORDS[Math.floor(Math.random() * WORDS.length)];
}


/* ── GAME LOGIC ──────────────────────────────────────────────*/

const ROWS = 6;
const COLS = 5;

/** @type {{ targetWord: string, currentRow: number, currentCol: number, guesses: string[], feedback: string[][], state: 'playing'|'win'|'lose' }} */
let game = {};

function initGame() {
  game = {
    targetWord: pickRandomWord(),
    currentRow: 0,
    currentCol: 0,
    guesses:  Array.from({ length: ROWS }, () => ""),
    feedback: Array.from({ length: ROWS }, () => []),
    state: "playing"
  };
}

/**
 * Add a letter to the current guess.
 * Returns true if the letter was accepted.
 */
function addLetter(letter) {
  if (game.state !== "playing") return false;
  if (game.currentCol >= COLS) return false;
  game.guesses[game.currentRow] += letter;
  game.currentCol++;
  return true;
}

/**
 * Remove the last letter from the current guess.
 * Returns true if there was a letter to remove.
 */
function removeLetter() {
  if (game.state !== "playing") return false;
  if (game.currentCol === 0) return false;
  game.guesses[game.currentRow] = game.guesses[game.currentRow].slice(0, -1);
  game.currentCol--;
  return true;
}

/**
 * Submit the current guess.
 * Returns "short" | "accepted"
 */
function submitGuess() {
  if (game.state !== "playing") return "invalid";
  if (game.currentCol < COLS) return "short";

  const guess    = game.guesses[game.currentRow];
  const target   = game.targetWord;
  const feedback = evaluateGuess(guess, target);

  game.feedback[game.currentRow] = feedback;

  if (guess === target) {
    game.state = "win";
  } else if (game.currentRow === ROWS - 1) {
    game.state = "lose";
  } else {
    game.currentRow++;
    game.currentCol = 0;
  }

  return "accepted";
}

/**
 * Score each letter of a guess against the target.
 * Returns an array of "correct" | "present" | "absent" for each position.
 */
function evaluateGuess(guess, target) {
  const result     = Array(COLS).fill("absent");
  const targetLeft = target.split("");   // tracks unmatched target letters
  const guessLeft  = guess.split("");

  // First pass: correct positions
  for (let i = 0; i < COLS; i++) {
    if (guessLeft[i] === targetLeft[i]) {
      result[i]    = "correct";
      targetLeft[i] = null;
      guessLeft[i]  = null;
    }
  }

  // Second pass: present (right letter, wrong position)
  for (let i = 0; i < COLS; i++) {
    if (guessLeft[i] === null) continue;
    const idx = targetLeft.indexOf(guessLeft[i]);
    if (idx !== -1) {
      result[i]    = "present";
      targetLeft[idx] = null;
    }
  }

  return result;
}

/** Returns a human-readable status string based on game state. */
function getStatusMessage() {
  if (game.state === "win")  return `You got it! The word was ${game.targetWord}.`;
  if (game.state === "lose") return `Game over! The word was ${game.targetWord}.`;
  if (game.currentRow === 0 && game.currentCol === 0) return "Type a word to begin.";
  return "";
}


/* ── UI (Document Object Model Layer) ──────────────────────────────────────────*/

const boardEl      = document.getElementById("board");
const statusEl     = document.getElementById("status");
const restartBtn   = document.getElementById("restart-btn");

/** Build the blank 6×5 grid of tiles once. */
function buildBoard() {
  boardEl.innerHTML = "";
  for (let r = 0; r < ROWS; r++) {
    const rowEl = document.createElement("div");
    rowEl.classList.add("row");
    rowEl.id = `row-${r}`;
    for (let c = 0; c < COLS; c++) {
      const tile = document.createElement("div");
      tile.classList.add("tile");
      tile.id = `tile-${r}-${c}`;
      rowEl.appendChild(tile);
    }
    boardEl.appendChild(rowEl);
  }
}

/** Return the tile element at a given row and column. */
function getTile(r, c) {
  return document.getElementById(`tile-${r}-${c}`);
}

/** Return the row element at a given index. */
function getRow(r) {
  return document.getElementById(`row-${r}`);
}

/**
 * Full render — syncs every tile to the current game state.
 * Called after each input event.
 */
function renderGame() {
  for (let r = 0; r < ROWS; r++) {
    const guess    = game.guesses[r];
    const feedback = game.feedback[r];

    for (let c = 0; c < COLS; c++) {
      const tile = getTile(r, c);
      const letter = guess[c] || "";

      tile.textContent = letter;

      // Clear all state classes before re-applying
      tile.classList.remove("filled", "correct", "present", "absent");

      if (feedback && feedback[c]) {
        tile.classList.add(feedback[c]);
      } else if (letter) {
        tile.classList.add("filled");
      }
    }
  }

  // Status message
  const msg = getStatusMessage();
  statusEl.textContent = msg;
  statusEl.className   = "status";
  if (game.state === "win")  statusEl.classList.add("win");
  if (game.state === "lose") statusEl.classList.add("lose");
}

/** Animate tiles flipping in sequence when a row is submitted. */
function animateRowFlip(row) {
  for (let c = 0; c < COLS; c++) {
    const tile = getTile(row, c);
    setTimeout(() => tile.classList.add("flip"), c * 80);
    setTimeout(() => tile.classList.remove("flip"), c * 80 + 400);
  }
}

/** Animate a tile popping when a letter is typed. */
function animateTilePop(row, col) {
  const tile = getTile(row, col);
  tile.classList.add("pop");
  setTimeout(() => tile.classList.remove("pop"), 120);
}

/** Shake the current row for an invalid submission attempt. */
function animateRowShake(row) {
  const rowEl = getRow(row);
  rowEl.classList.add("shake");
  setTimeout(() => rowEl.classList.remove("shake"), 400);
}


/* ── INPUT HANDLER ───────────────────────────────────────────
   Converts raw keyboard events into logic calls + renders.
   ─────────────────────────────────────────────────────────── */

function processInput(key) {
  if (game.state !== "playing") return;

  if (key === "BACKSPACE") {
    removeLetter();
    renderGame();
    return;
  }

  if (key === "ENTER") {
    const rowBeforeSubmit = game.currentRow;
    const result = submitGuess();

    if (result === "short") {
      animateRowShake(game.currentRow);
      statusEl.textContent = "Not enough letters.";
      return;
    }

    if (result === "accepted") {
      animateRowFlip(rowBeforeSubmit);
      // Delay render so flip animation starts before colors are applied
      setTimeout(() => renderGame(), COLS * 80 + 100);
    }
    return;
  }

  // Single letter A–Z
  if (/^[A-Z]$/.test(key)) {
    const col = game.currentCol;
    if (addLetter(key)) {
      renderGame();
      animateTilePop(game.currentRow, col);
    }
  }
}

document.addEventListener("keydown", (e) => {
  const key = e.key.toUpperCase();
  // Ignore modifier combos (Ctrl+C etc.)
  if (e.ctrlKey || e.metaKey || e.altKey) return;
  processInput(key);
});


/* ── RESTART ─────────────────────────────────────────────────── */

function restartGame() {
  initGame();
  buildBoard();
  renderGame();
}

restartBtn.addEventListener("click", restartGame);


/* ── INIT ─────────────────────────────────────────────────────── */

restartGame();