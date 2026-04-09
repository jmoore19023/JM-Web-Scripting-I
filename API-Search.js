
const searchBtn   = document.getElementById("searchBtn");
const searchInput = document.getElementById("searchInput");
const statusEl    = document.getElementById("status");
const resultsEl   = document.getElementById("results");

const API_BASE = "https://www.themealdb.com/api/json/v1/1/search.php";

// ── Event Listeners ──────────────────────────────────────────

searchBtn.addEventListener("click", runSearch);

// Also trigger search on Enter key
searchInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") runSearch();
});

// ── Main Search Function ──────────────────────────────────────

async function runSearch() {
  const term = searchInput.value.trim();

  // Validate: don't allow empty searches
  if (!term) {
    setStatus("Please enter a search term.", "error");
    resultsEl.innerHTML = "";
    return;
  }

  setStatus("Loading...", "loading");
  resultsEl.innerHTML = "";
  searchBtn.disabled = true;

  try {
    const url = `${API_BASE}?s=${encodeURIComponent(term)}`;
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Network error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    displayResults(data, term);

  } catch (error) {
    console.error("Fetch error:", error);
    setStatus("Something went wrong. Please check your connection and try again.", "error");
  } finally {
    searchBtn.disabled = false;
  }
}

// ── Display Results ───────────────────────────────────────────

function displayResults(data, term) {
  if (!data.meals || data.meals.length === 0) {
    setStatus(`No results found for "${term}". Try a different search term.`, "");
    return;
  }

  const count = data.meals.length;
  setStatus(`Found ${count} result${count !== 1 ? "s" : ""} for "${term}"`, "");

  const cards = data.meals.map(buildCard).join("");
  resultsEl.innerHTML = cards;
}

// ── Build a Single Meal Card ──────────────────────────────────

function buildCard(meal) {
  const title    = escapeHtml(meal.strMeal    || "Unknown Meal");
  const category = escapeHtml(meal.strCategory || "Uncategorized");
  const area     = escapeHtml(meal.strArea     || "Unknown Origin");
  const imgSrc   = meal.strMealThumb || "";
  const imgAlt   = `Photo of ${title}`;
  const sourceUrl = meal.strSource || meal.strYoutube || null;
  const mealId    = meal.idMeal;

  const imgMarkup = imgSrc
    ? `<img class="meal-card__img" src="${imgSrc}" alt="${imgAlt}" loading="lazy" />`
    : `<div class="meal-card__img" style="background:var(--rust-light);display:flex;align-items:center;justify-content:center;font-size:2rem;">🍽️</div>`;

  const sourceLine = sourceUrl
    ? `<p class="meal-card__source"><a href="${escapeHtml(sourceUrl)}" target="_blank" rel="noopener">View full recipe ↗</a></p>`
    : mealId
    ? `<p class="meal-card__source"><a href="https://www.themealdb.com/meal/${mealId}" target="_blank" rel="noopener">View on TheMealDB ↗</a></p>`
    : "";

  return `
    <article class="meal-card">
      <div class="meal-card__image-wrap">
        ${imgMarkup}
        <span class="meal-card__badge">${area}</span>
      </div>
      <div class="meal-card__body">
        <h2 class="meal-card__title">${title}</h2>
        <div class="meal-card__meta">
          <span class="meta-tag">${category}</span>
          <span class="meta-tag">${area}</span>
        </div>
        ${sourceLine}
      </div>
    </article>
  `;
}

// ── Status Helper ─────────────────────────────────────────────

function setStatus(message, type) {
  statusEl.className = "status-message";

  if (type === "error") {
    statusEl.classList.add("is-error");
    statusEl.textContent = message;
  } else if (type === "loading") {
    statusEl.classList.add("is-loading");
    statusEl.innerHTML = `<span class="spinner" aria-hidden="true"></span><span>${message}</span>`;
  } else {
    statusEl.textContent = message;
  }
}

// ── Security: Escape HTML to prevent XSS ─────────────────────

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}