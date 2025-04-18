let soundEnabled = false;

function toggleSound() {
  soundEnabled = !soundEnabled;
  alert("音效已" + (soundEnabled ? "啟用" : "關閉"));
}

async function fetchData() {
  const res = await fetch('/api/stocks');
  const data = await res.json();
  const tbody = document.querySelector("#stockTable tbody");
  tbody.innerHTML = "";
  data.forEach(stock => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${stock.code}</td>
      <td>${stock.name}</td>
      <td>${stock.price}</td>
      <td>${stock.direction}</td>
      <td>${stock.ai_win_rate}</td>
      <td>${stock.entry}</td>
      <td>${stock.exit}</td>
      <td>${stock.sim}</td>`;
    tbody.appendChild(tr);
  });
}

setInterval(fetchData, 1000);