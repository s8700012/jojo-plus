setInterval(() => {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('table-body');
            tbody.innerHTML = '';
            data.forEach(stock => {
                const row = `<tr>
                    <td>${stock.code}</td><td>${stock.name}</td><td>${stock.price}</td>
                    <td>${stock.direction}</td><td>${stock.ai_win_rate}</td>
                    <td>${stock.entry}</td><td>${stock.exit}</td><td>${stock.sim}</td>
                </tr>`;
                tbody.innerHTML += row;
            });
        });
}, 1000);