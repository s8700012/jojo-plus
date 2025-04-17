function toggleSound() { alert('音效功能尚在開發中'); }
function fetchData() {
 fetch('/data')
  .then(r => r.json())
  .then(data => {
    const table = document.getElementById('stock-table');
    table.innerHTML = '<tr><th>代號</th><th>名稱</th><th>價格</th><th>方向</th><th>進場</th><th>出場</th><th>AI勝率</th></tr>' +
      data.map(s => `<tr><td>${s.symbol}</td><td>${s.name}</td><td>${s.price}</td><td>${s.direction}</td><td>${s.entry}</td><td>${s.exit}</td><td>${s.winrate}%</td></tr>`).join('');
  });
}
setInterval(fetchData, 1000);