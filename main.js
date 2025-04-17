async function fetchStocks() {
    try {
        const response = await fetch('/stocks.json');
        const stocks = await response.json();
        const tableBody = document.querySelector('#stock-table tbody');
        tableBody.innerHTML = ''; // 清空原有表格

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
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('載入股票資料時發生錯誤：', error);
    }
}

// 每秒更新一次
setInterval(fetchStocks, 1000);

// 頁面初始載入時也要呼叫一次
fetchStocks();
