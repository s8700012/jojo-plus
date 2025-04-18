
let audioEnabled = false;

function toggleAudio() {
  audioEnabled = !audioEnabled;
  alert(audioEnabled ? '音效已啟用' : '音效已關閉');
}

function playSound() {
  if (audioEnabled) {
    const audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
    audio.play();
  }
}

async function fetchStocks() {
  try {
    const response = await fetch('/stocks.json');
    const stocks = await response.json();
    const tbody = document.querySelector('#stockTable tbody');
    tbody.innerHTML = '';
    stocks.forEach(stock => {
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
    playSound();
  } catch (error) {
    console.error('資料載入失敗:', error);
  }
}

setInterval(fetchStocks, 1000);
