# Yahoo Proxy Server for 台股即時報價

## 一、部署 Render 步驟

1. 登入 https://dashboard.render.com
2. 點選 [New] → [Web Service]
3. 選擇 "Deploy from a GitHub repo" 或 "Upload directory"
4. 設定參數：
   - Name: yahoo-proxy-server
   - Runtime: Node
   - Build command: `npm install`
   - Start command: `node index.js`
   - Region: Asia (可選)
5. 點 Deploy 即可！

## 二、API 使用方式

- 檢查服務是否正常：
  ```
  GET /
  ```

- 查詢股價：
  ```
  GET /quote?symbol=2330
  ```

  若查詢台積電，URL 會是：
  `https://your-render-domain.onrender.com/quote?symbol=2330`

## 三、注意

- symbol 請輸入股票代碼（不含 .TW），系統自動加上 .TW。
