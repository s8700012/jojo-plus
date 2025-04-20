const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');
const cors = require('cors');

const app = express();
app.use(cors());

app.get('/', (req, res) => {
  res.send('Yahoo Proxy Server 正常運作中！');
});

app.get('/quote', async (req, res) => {
  const symbol = req.query.symbol;
  if (!symbol) {
    return res.status(400).json({ error: '缺少 symbol 參數' });
  }

  const url = `https://tw.stock.yahoo.com/quote/${symbol}.TW`;

  try {
    const response = await axios.get(url, {
      headers: { 'User-Agent': 'Mozilla/5.0' }
    });

    const $ = cheerio.load(response.data);
    let priceText =
      $('fin-streamer[data-field="regularMarketPrice"]').first().text() ||
      $('span:contains("成交")').next().text();

    priceText = priceText.replace(/,/g, '').trim();

    if (!priceText || isNaN(priceText)) {
      console.log(`[DEBUG] ${symbol} 抓到異常價格: ${priceText}`);
      return res.status(404).json({ error: '找不到價格' });
    }

    res.json({
      symbol: symbol,
      price: parseFloat(priceText)
    });

  } catch (err) {
    console.error(`[錯誤] 抓取 ${symbol} 價格失敗:`, err.message);
    res.status(500).json({ error: '伺服器錯誤' });
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`伺服器啟動於 http://localhost:${port}`);
});
