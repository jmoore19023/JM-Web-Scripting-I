const go = document.getElementById("go");
const out = document.getElementById("out");

  function createTable(cities) {
    let html = '<table border = "1">';
    html += '<thead><tr><th>Order</th><th>Doomed Cities</th></tr></thead>';
    for (let i = 0; i < cities.length; i++) {
      html += `<tr><td>${i + 1}</td><td>${cities[i]}</td></tr>`;
      
    }
    html += "</table>";
    out.innerHTML = html;
  }


go.addEventListener('click', () => {
  const cities = [];

  for (let i = 1; i <= 5; i++) {
    let city = prompt(`City #${i}:`);

    if (city === null) {
      out.textContent = 'Cancelled.';
      return;
    }

    city = city.trim();
    if (!city) {
      i -= 1;
      alert('Please type a city name.');
      continue;
    }

    cities.push(city);
  }

  createTable(cities);
});