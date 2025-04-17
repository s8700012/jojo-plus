let audioEnabled = false;
function toggleAudio() {
    audioEnabled = !audioEnabled;
    alert("音效已 " + (audioEnabled ? "啟用" : "關閉"));
}
async function fetchPrices() {
    const res = await fetch('/api/prices');
    const data = await res.json();
    const tbody = document.querySelector("#stock-table tbody");
    tbody.innerHTML = "";
    data.forEach(stock => {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${stock.symbol}</td><td>${stock.name}</td><td>${stock.price.toFixed(2)}</td><td>${stock.direction}</td><td>${stock.probability}%</td>`;
        tbody.appendChild(row);
    });
}
setInterval(fetchPrices, 1000);
fetchPrices();
