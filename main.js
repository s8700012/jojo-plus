let audioEnabled = false;

function toggleAudio() {
    audioEnabled = !audioEnabled;
    alert(audioEnabled ? '音效已啟用' : '音效已關閉');
}

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

    if (audioEnabled) {
        const audio = new Audio('https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg');
        audio.play();
    }
}

setInterval(fetchData, 1000);
fetchData();
