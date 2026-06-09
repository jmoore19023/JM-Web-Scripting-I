/* =============================================
   app.js — UI Layer
   Handles all DOM updates and user interactions.
   Relies on functions from habits.js.
============================================= */


// ── Filter State ─────────────────────────────────

// Tracks which filter is active: 'all', 'incomplete', or 'done'
// Defaults to 'incomplete' so completed habits are hidden automatically
let activeFilter = 'incomplete';


// ── On Page Load ─────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    showTodayDate();
    initFilter();
    renderAll();
});


// ── Theme Toggle ─────────────────────────────────

function initTheme() {
    const html      = document.documentElement;
    const toggleBtn = document.getElementById('themeToggle');
    const icon      = toggleBtn.querySelector('.theme-icon');

    // Load saved theme (shared key with main site)
    const saved = localStorage.getItem('theme');
    if (saved) {
        html.setAttribute('data-theme', saved);
        icon.textContent = saved === 'dark' ? '☀' : '☾';
    }

    toggleBtn.addEventListener('click', () => {
        const current = html.getAttribute('data-theme');
        const next    = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        icon.textContent = next === 'dark' ? '☀' : '☾';
        toggleBtn.setAttribute('aria-label', next === 'dark' ? 'Toggle light mode' : 'Toggle dark mode');
    });
}


// ── Date Display ─────────────────────────────────

function showTodayDate() {
    const el = document.getElementById('todayDate');
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    el.textContent = new Date().toLocaleDateString('en-US', options);
}


// ── Filter Buttons ───────────────────────────────

function initFilter() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            activeFilter = btn.dataset.filter;

            // Update which button looks active
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Re-render only the list (filter doesn't affect progress bar or weekly grid)
            const habits = loadHabits();
            renderHabitList(habits);
        });
    });

    // Set the default active button on load
    const defaultBtn = document.querySelector(`.filter-btn[data-filter="${activeFilter}"]`);
    if (defaultBtn) defaultBtn.classList.add('active');
}


// ── Add Habit Form ───────────────────────────────

document.getElementById('addHabitForm').addEventListener('submit', (e) => {
    e.preventDefault();

    const input   = document.getElementById('habitInput');
    const value   = input.value.trim();

    // Validation: blank input
    if (!value) {
        showError('Please enter a habit name.');
        return;
    }

    // Validation: duplicate name (case-insensitive)
    const existing    = loadHabits();
    const isDuplicate = existing.some(h => h.name.toLowerCase() === value.toLowerCase());
    if (isDuplicate) {
        showError('That habit already exists.');
        return;
    }

    clearError();
    addHabit(value);
    input.value = '';
    renderAll();
});

function showError(message) {
    document.getElementById('formError').textContent = message;
}

function clearError() {
    document.getElementById('formError').textContent = '';
}


// ── Render Everything ────────────────────────────

// Central render — rebuilds all three sections
function renderAll() {
    const habits = loadHabits();
    renderProgressSummary(habits);
    renderProgressBar(habits);
    renderHabitList(habits);
    renderWeeklyGrid(habits);
}


// ── Progress Summary ─────────────────────────────

function renderProgressSummary(habits) {
    const el = document.getElementById('progressSummary');

    if (habits.length === 0) {
        el.textContent = 'No habits yet. Add one below!';
        el.classList.remove('all-done');
        return;
    }

    const { done, total } = getTodayProgress(habits);

    if (done === total) {
        el.textContent = `✓ All ${total} habit${total !== 1 ? 's' : ''} done today — great work!`;
        el.classList.add('all-done');
    } else {
        el.textContent = `${done} of ${total} habit${total !== 1 ? 's' : ''} done today`;
        el.classList.remove('all-done');
    }
}


// ── Progress Bar ─────────────────────────────────

function renderProgressBar(habits) {
    const wrap  = document.getElementById('progressBarWrap');
    const fill  = document.getElementById('progressBarFill');
    const label = document.getElementById('progressBarLabel');

    // Hide the bar if no habits
    if (habits.length === 0) {
        wrap.style.display = 'none';
        return;
    }

    const { done, total } = getTodayProgress(habits);
    const pct = Math.round((done / total) * 100);

    wrap.style.display = 'block';

    // Set the bar width — CSS transition handles the animation
    fill.style.width = pct + '%';
    label.textContent = pct + '%';

    // Turn the bar green when fully complete
    if (pct === 100) {
        fill.classList.add('complete');
    } else {
        fill.classList.remove('complete');
    }
}


// ── Habit List ───────────────────────────────────

function renderHabitList(habits) {
    const list       = document.getElementById('habitList');
    const emptyState = document.getElementById('emptyState');

    list.innerHTML = '';

    if (habits.length === 0) {
        emptyState.style.display = 'block';
        emptyState.textContent   = 'You haven\'t added any habits yet.';
        return;
    }

    emptyState.style.display = 'none';

    const today = getTodayKey();

    // Apply the active filter
    const filtered = habits.filter(habit => {
        const isDone = habit.history[today] && habit.history[today].done;
        if (activeFilter === 'done')       return isDone;
        if (activeFilter === 'incomplete') return !isDone;
        return true; // 'all'
    });

    // Smart empty message when filter returns nothing
    if (filtered.length === 0) {
        emptyState.style.display = 'block';
        emptyState.textContent   = activeFilter === 'done'
            ? 'No completed habits yet today.'
            : 'All habits are done for today!';
        return;
    }

    emptyState.textContent = 'You haven\'t added any habits yet.';

    filtered.forEach((habit, index) => {
        const isDone = habit.history[today] && habit.history[today].done;
        const note   = habit.history[today] ? habit.history[today].note : '';
        const streak = getStreak(habit);

        // Find the real index in the full array for reorder buttons
        const realIndex  = habits.indexOf(habit);
        const isFirst    = realIndex === 0;
        const isLast     = realIndex === habits.length - 1;

        const li = document.createElement('li');
        li.className = `habit-item${isDone ? ' is-done' : ''}`;

        li.innerHTML = `
            <div class="habit-main">

                <!-- Up/Down reorder buttons -->
                <div class="reorder-btns">
                    <button
                        class="reorder-btn"
                        data-id="${habit.id}"
                        data-dir="up"
                        aria-label="Move habit up"
                        ${isFirst ? 'disabled' : ''}>▲</button>
                    <button
                        class="reorder-btn"
                        data-id="${habit.id}"
                        data-dir="down"
                        aria-label="Move habit down"
                        ${isLast ? 'disabled' : ''}>▼</button>
                </div>

                <!-- Checkbox to mark done -->
                <button
                    class="check-btn${isDone ? ' checked' : ''}"
                    aria-label="${isDone ? 'Mark incomplete' : 'Mark complete'}"
                    data-id="${habit.id}">
                    ${isDone ? '✓' : ''}
                </button>

                <!-- Habit name (or edit input when editing) -->
                <span class="habit-name" id="name-${habit.id}">${escapeHtml(habit.name)}</span>

                <!-- Streak badge — only show if streak > 0 -->
                ${streak > 0
                    ? `<span class="streak-badge" title="${streak} day streak">🔥 ${streak}</span>`
                    : ''}

                <!-- Edit + Delete buttons -->
                <div class="habit-actions">
                    <button class="action-btn edit-btn"   data-id="${habit.id}" aria-label="Edit habit name">✎</button>
                    <button class="action-btn delete-btn" data-id="${habit.id}" aria-label="Delete habit">✕</button>
                </div>
            </div>

            <!-- Optional note for today -->
            <div class="note-row">
                <input
                    type="text"
                    class="note-input"
                    placeholder="Add a note for today (optional)"
                    maxlength="120"
                    data-id="${habit.id}"
                    value="${escapeHtml(note)}"
                    aria-label="Note for ${escapeHtml(habit.name)}">
            </div>
        `;

        list.appendChild(li);
    });

    attachHabitListeners();
}


// ── Event Listeners for Habit Items ─────────────

function attachHabitListeners() {

    // Reorder buttons
    document.querySelectorAll('.reorder-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const id  = Number(btn.dataset.id);
            const dir = btn.dataset.dir;
            if (dir === 'up') {
                moveHabitUp(id);
            } else {
                moveHabitDown(id);
            }
            renderAll();
        });
    });

    // Check/uncheck buttons
    document.querySelectorAll('.check-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = Number(btn.dataset.id);
            toggleHabit(id);
            renderAll();
        });
    });

    // Delete buttons
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = Number(btn.dataset.id);
            deleteHabit(id);
            renderAll();
        });
    });

    // Edit buttons — swap name text to an input field
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const id      = Number(btn.dataset.id);
            const nameEl  = document.getElementById(`name-${id}`);
            const current = nameEl.textContent;

            nameEl.innerHTML = `
                <input
                    type="text"
                    class="edit-input"
                    value="${escapeHtml(current)}"
                    maxlength="60"
                    aria-label="Edit habit name">
            `;

            const editInput = nameEl.querySelector('.edit-input');
            editInput.focus();
            editInput.select();

            function saveEdit() {
                const newName = editInput.value.trim();

                if (!newName) {
                    showError('Habit name cannot be blank.');
                    renderAll();
                    return;
                }

                const habits      = loadHabits();
                const isDuplicate = habits.some(h => h.id !== id && h.name.toLowerCase() === newName.toLowerCase());
                if (isDuplicate) {
                    showError('That habit name already exists.');
                    renderAll();
                    return;
                }

                clearError();
                renameHabit(id, newName);
                renderAll();
            }

            editInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter')  saveEdit();
                if (e.key === 'Escape') renderAll();
            });

            editInput.addEventListener('blur', saveEdit);
        });
    });

    // Note inputs — save silently on blur
    document.querySelectorAll('.note-input').forEach(input => {
        input.addEventListener('blur', () => {
            const id = Number(input.dataset.id);
            saveNote(id, input.value);
        });
    });
}


// ── Weekly Grid ──────────────────────────────────

function renderWeeklyGrid(habits) {
    const grid    = document.getElementById('weeklyGrid');
    const section = document.getElementById('weeklySection');

    grid.innerHTML = '';

    if (habits.length === 0) {
        section.style.display = 'none';
        return;
    }

    section.style.display = 'block';

    const days = getLast7Days();

    habits.forEach(habit => {
        const row = document.createElement('div');
        row.className = 'week-row';

        const nameLabel = document.createElement('span');
        nameLabel.className   = 'week-label';
        nameLabel.textContent = habit.name;
        row.appendChild(nameLabel);

        const cells = document.createElement('div');
        cells.className = 'week-cells';

        days.forEach(dateKey => {
            const isDone   = habit.history[dateKey] && habit.history[dateKey].done;
            const isToday  = dateKey === getTodayKey();
            const dayLabel = getDayLabel(dateKey);

            const cell = document.createElement('div');
            cell.className = `week-cell${isDone ? ' week-cell--done' : ''}${isToday ? ' week-cell--today' : ''}`;
            cell.setAttribute('title', `${dateKey}: ${isDone ? 'Done ✓' : 'Not done'}`);
            cell.innerHTML = `
                <span class="week-day">${dayLabel}</span>
                <span class="week-dot">${isDone ? '✓' : ''}</span>
            `;
            cells.appendChild(cell);
        });

        row.appendChild(cells);
        grid.appendChild(row);
    });
}


// ── Utility ──────────────────────────────────────

// Prevents XSS by escaping user-entered HTML characters
function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}