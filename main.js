async function fetchStocks() {
  const res = await fetch('/api/stocks');
  const data = await res.json();

  const tbody = document.getElementById('stock-table-body');
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

setInterval(fetchStocks, 1000);
fetchStocks();