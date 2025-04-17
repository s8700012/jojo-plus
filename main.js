
let soundEnabled = true;
function toggleSound() {
  soundEnabled = !soundEnabled;
  alert(soundEnabled ? "音效已啟用" : "音效已關閉");
}
async function fetchData() {
  const res = await fetch("/api/data");
  const data = await res.json();
  const tbody = document.querySelector("#stock-table tbody");
  tbody.innerHTML = "";
  data.forEach((stock) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${stock.symbol}</td>
      <td>${stock.name}</td>
      <td>${stock.price.toFixed(2)}</td>
      <td>${stock.direction}</td>
      <td>${stock.accuracy}%</td>
    `;
    tbody.appendChild(tr);
  });
  if (soundEnabled) new Audio("https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg").play();
}
setInterval(fetchData, 1000);
