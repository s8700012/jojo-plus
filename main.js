let audioEnabled = false;

function toggleAudio() {
    audioEnabled = !audioEnabled;
    alert("音效功能：" + (audioEnabled ? "啟用" : "關閉"));
}

function fetchStocks() {
    fetch('/stocks')
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector("#stockTable tbody");
            tbody.innerHTML = '';
            data.forEach(stock => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${stock.symbol}</td>
                    <td>${stock.name}</td>
                    <td>${stock.price}</td>
                    <td>${stock.direction}</td>
                    <td>${stock.ai_win_rate}%</td>
                    <td>${stock.entry_price}</td>
                    <td>${stock.exit_price}</td>
                `;
                tbody.appendChild(row);
            });
        });
}

setInterval(fetchStocks, 1000);