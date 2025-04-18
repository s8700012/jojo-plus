let audioEnabled = false;
function toggleAudio() {
  audioEnabled = !audioEnabled;
  alert(audioEnabled ? "音效已啟用" : "音效已關閉");
}

async function fetchData() {
  const res = await fetch('/data');
  const data = await res.json();
  const tbody = document.querySelector('#stockTable tbody');
  tbody.innerHTML = '';
  data.forEach(item => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${item.code}</td>
      <td>${item.name}</td>
      <td>${item.price}</td>
      <td>${item.direction}</td>
      <td>${item.ai_win_rate}</td>
      <td>${item.entry}</td>
      <td>${item.exit}</td>
      <td>${item.sim}</td>
    `;
    tbody.appendChild(row);
    if (audioEnabled && parseFloat(item.ai_win_rate) > 85) {
      const audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
      audio.play();
    }
  });
}
setInterval(fetchData, 1000);
fetchData();