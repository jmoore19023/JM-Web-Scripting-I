/* =============================================
   habits.js — Data Layer
   Handles all data operations: loading, saving,
   and updating habits in localStorage.

   Data structure stored in localStorage:
   habits = [
     {
       id: 1234567890,          // unique timestamp ID
       name: "Drink water",     // habit name
       history: {               // keyed by date string "YYYY-MM-DD"
         "2026-05-01": {
           done: true,
           note: "Finished early!"
         }
       }
     },
     ...
   ]
============================================= */


// ── Helpers ─────────────────────────────────────

// Returns today's date as a "YYYY-MM-DD" string
function getTodayKey() {
    const d = new Date();
    const yyyy = d.getFullYear();
    const mm   = String(d.getMonth() + 1).padStart(2, '0');
    const dd   = String(d.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
}

// Returns the last 7 date keys including today, oldest first
function getLast7Days() {
    const days = [];
    for (let i = 6; i >= 0; i--) {
        const d = new Date();
        d.setDate(d.getDate() - i);
        const yyyy = d.getFullYear();
        const mm   = String(d.getMonth() + 1).padStart(2, '0');
        const dd   = String(d.getDate()).padStart(2, '0');
        days.push(`${yyyy}-${mm}-${dd}`);
    }
    return days;
}

// Returns a short day label like "Mon", "Tue" from a date key
function getDayLabel(dateKey) {
    const [yyyy, mm, dd] = dateKey.split('-').map(Number);
    const date = new Date(yyyy, mm - 1, dd);
    return date.toLocaleDateString('en-US', { weekday: 'short' });
}


// ── Load & Save ──────────────────────────────────

// Loads habit array from localStorage (returns [] if nothing saved)
function loadHabits() {
    const saved = localStorage.getItem('habits');
    return saved ? JSON.parse(saved) : [];
}

// Saves the habit array to localStorage
function saveHabits(habits) {
    localStorage.setItem('habits', JSON.stringify(habits));
}


// ── CRUD Operations ──────────────────────────────

// Adds a new habit and saves. Returns updated array.
function addHabit(name) {
    const habits = loadHabits();
    const newHabit = {
        id:      Date.now(),   // unique ID based on timestamp
        name:    name.trim(),
        history: {}
    };
    habits.push(newHabit);
    saveHabits(habits);
    return habits;
}

// Removes a habit by ID and saves. Returns updated array.
function deleteHabit(id) {
    let habits = loadHabits();
    habits = habits.filter(h => h.id !== id);
    saveHabits(habits);
    return habits;
}

// Updates a habit's name by ID and saves. Returns updated array.
function renameHabit(id, newName) {
    const habits = loadHabits();
    const habit  = habits.find(h => h.id === id);
    if (habit) {
        habit.name = newName.trim();
        saveHabits(habits);
    }
    return habits;
}

// Toggles the done state for a habit on today's date. Returns updated array.
function toggleHabit(id) {
    const habits   = loadHabits();
    const habit    = habits.find(h => h.id === id);
    const today    = getTodayKey();

    if (habit) {
        // If no entry for today yet, create one
        if (!habit.history[today]) {
            habit.history[today] = { done: false, note: '' };
        }
        // Flip the done flag
        habit.history[today].done = !habit.history[today].done;
        saveHabits(habits);
    }
    return habits;
}

// Saves a note for a habit on today's date. Returns updated array.
function saveNote(id, noteText) {
    const habits = loadHabits();
    const habit  = habits.find(h => h.id === id);
    const today  = getTodayKey();

    if (habit) {
        if (!habit.history[today]) {
            habit.history[today] = { done: false, note: '' };
        }
        habit.history[today].note = noteText.trim();
        saveHabits(habits);
    }
    return habits;
}


// ── Stats ────────────────────────────────────────

// Returns the current streak (consecutive days ending today) for one habit
function getStreak(habit) {
    let streak = 0;
    const today = new Date();

    for (let i = 0; i < 365; i++) {
        const d = new Date(today);
        d.setDate(d.getDate() - i);
        const yyyy = d.getFullYear();
        const mm   = String(d.getMonth() + 1).padStart(2, '0');
        const dd   = String(d.getDate()).padStart(2, '0');
        const key  = `${yyyy}-${mm}-${dd}`;

        if (habit.history[key] && habit.history[key].done) {
            streak++;
        } else {
            break; // streak is broken
        }
    }
    return streak;
}

// Returns how many habits are done today out of total
function getTodayProgress(habits) {
    const today = getTodayKey();
    const done  = habits.filter(h => h.history[today] && h.history[today].done).length;
    return { done, total: habits.length };
}


// ── Reorder ──────────────────────────────────────

// Moves a habit one position up in the array. Returns updated array.
function moveHabitUp(id) {
    const habits = loadHabits();
    const index  = habits.findIndex(h => h.id === id);
    // Can't move up if already at the top
    if (index <= 0) return habits;
    // Swap with the item above
    [habits[index - 1], habits[index]] = [habits[index], habits[index - 1]];
    saveHabits(habits);
    return habits;
}

// Moves a habit one position down in the array. Returns updated array.
function moveHabitDown(id) {
    const habits = loadHabits();
    const index  = habits.findIndex(h => h.id === id);
    // Can't move down if already at the bottom
    if (index === -1 || index === habits.length - 1) return habits;
    // Swap with the item below
    [habits[index], habits[index + 1]] = [habits[index + 1], habits[index]];
    saveHabits(habits);
    return habits;
}