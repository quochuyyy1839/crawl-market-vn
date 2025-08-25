# Market Data Notification Bot 📊

A comprehensive bot that fetches Vietnamese market data and sends separate notifications to Telegram for each data type. Built with vnstock library for accurate and real-time data.

## Features 🚀

- **📈 Vietnamese Stock Prices**: Real-time prices from VCI source
- **📊 VN-Index**: Market index with daily changes  
- **🥇 Gold Prices**: SJC gold buy/sell rates
- **💱 Exchange Rates**: VCB foreign exchange rates
- **₿ Cryptocurrency**: Bitcoin and Ethereum prices

## Installation 🛠️

1. **Clone the repository:**
   ```bash
   git clone https://github.com/quochuyyy1839/crawl-price-gold.git
   cd crawl-price-gold
   ```

2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Setup environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Telegram bot credentials
   ```

## Configuration ⚙️

Create a `.env` file with the following variables:

```env
# Telegram Bot Config
TOKEN=your_bot_token_here
CHAT_ID=your_chat_id_here

# Feature Toggles (true/false)
STOCK_PRICE=true
VNINDEX=true
GOLD_PRICE=true
EXCHANGE_RATE=true
CRYPTO_PRICE=true

# Symbols to track
STOCK=VCB,VIC,HPG,VHM,MSN,TCB
GOLD=SJC
CRYPTO=BTC,ETH
EXCHANGE=USD,EUR,JPY
```

### Feature Toggles
- Set any feature to `false` to disable that notification
- Customize symbols by modifying the comma-separated lists

## Usage 🎯

**Run the bot:**
```bash
python3 main.py
```

**Test individual features:**
```bash
python3 stock_price.py  # Console output for testing
```

The bot will send **5 separate messages** to your Telegram chat:
1. Stock prices with current VND rates
2. VN-Index with daily change percentage  
3. SJC gold buy/sell prices
4. VCB exchange rates for major currencies
5. Crypto prices with 24h change

## Message Format 📱

All messages use **Markdown formatting** with:
- **Bold headers** with emojis
- `Code blocks` for clean data display
- Timestamps for each update
- Change indicators (+/-) with percentages

Example output:
```
📈 *CỔ PHIẾU VIỆT NAM*
```
VCB: 61,000 VND
VIC: 41,000 VND
HPG: 22,000 VND
```
_Cập nhật: 26/08/2025 00:30:15_
```

## Data Sources 📡

- **Stocks & Index**: vnstock library (VCI/MSN sources)
- **Gold**: vnstock SJC official rates
- **Exchange**: vnstock VCB official rates  
- **Crypto**: CoinGecko API for accurate pricing

## Docker Support 🐳

```bash
docker build -t market-data-bot .
docker run --env-file .env market-data-bot
```

## Project Structure 📁

```
├── main.py                     # Main bot script
├── config.py                   # Environment configuration
├── stock_price.py             # Console testing script
├── .env                       # Your configuration (create from .env.example)
├── services/
│   ├── market_data.py         # Data fetching with vnstock
│   ├── telegram_formatter.py  # Message formatting
│   └── telegram_bot.py        # Telegram API integration
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Contributing 🤝

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- [vnstock](https://github.com/thinh-vu/vnstock) - Vietnamese stock market data
- [CoinGecko](https://coingecko.com) - Cryptocurrency market data
