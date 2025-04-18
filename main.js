
async function fetchData() {
  const res = await fetch('/stocks.json');
  const data = await res.json();
  const tbody = document.querySelector('#stock-table tbody');
  tbody.innerHTML = '';
  data.forEach(stock => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${stock.code}</td>
      <td>${stock.name}</td>
      <td>${stock.price}</td>
      <td>${stock.direction}</td>
      <td>${stock.ai_win_rate}</td>
      <td>${stock.entry}</td>
      <td>${stock.exit}</td>
      <td>${stock.sim}</td>
    `;
    tbody.appendChild(row);
  });
}
setInterval(fetchData, 1000);
fetchData();
