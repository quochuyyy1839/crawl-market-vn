# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Core Commands
- **Run the application**: `python main.py` or `python3 main.py`
- **Install dependencies**: `pip install -r requirements.txt`
- **Test configuration**: Set `TELEGRAM_ENABLED=false` in `.env` to test locally without Telegram spam

### Environment Setup
- Copy `.env.example` to `.env` and configure your Telegram credentials
- For local development, set `TELEGRAM_ENABLED=false` to avoid sending messages during testing
- All market data is always printed to console regardless of Telegram settings

## Architecture Overview

This is a Vietnamese market data collection and notification bot built with a modular service-oriented architecture.

### Core Architecture Pattern
The application follows a **Data Collector + Service Pattern**:

1. **DataCollector** (`services/core/data_collector.py`) orchestrates all data fetching
2. **BaseMarketDataService** (`services/core/base_service.py`) provides abstract interface for all data sources
3. **Individual Services** implement specific data sources (stocks, crypto, gold, etc.)
4. **Configuration System** (`config/`) manages environment-based settings and feature toggles

### Service Structure
```
services/
├── core/                    # Core framework
│   ├── data_collector.py   # Main orchestrator
│   ├── base_service.py     # Abstract service interface
│   └── exceptions.py       # Custom exceptions
├── data_sources/           # Market data services
│   ├── stock_service.py    # Vietnamese stocks (vnstock VCI source)
│   ├── crypto_service.py   # Cryptocurrency (CryptoCompare API)
│   ├── gold_service.py     # SJC gold prices
│   ├── exchange_service.py # VCB foreign exchange rates
│   └── index_service.py    # VN-Index market index
└── telegram/               # Telegram integration
    ├── bot.py             # Async Telegram bot using python-telegram-bot
    └── formatter.py       # Message formatting with Markdown
```

### Key Architectural Decisions

**Service Registration Pattern**: Services are registered with the DataCollector along with their enabled status, allowing dynamic enable/disable via environment variables.

**Error Handling Strategy**: Each service extends BaseMarketDataService which provides consistent error handling. Errors don't stop other services from running.

**Configuration Management**: Two-layer config system:
- `config/settings.py` - Core Telegram settings
- `config/data_sources.py` - Feature toggles and symbols

**Data Flow**: main.py → DataCollector.collect_all() → Individual Services → Telegram Formatter → Telegram Bot

## Data Sources Integration

### vnstock Library
- **Stocks**: Uses VCI source with dynamic 30-day date ranges for real-time pricing
- **Gold**: SJC official rates
- **Exchange**: VCB official rates
- **VN-Index**: Market index data

### External APIs
- **Cryptocurrency**: CryptoCompare API with VCB USD/VND conversion for accurate local pricing

## Configuration System

### Feature Toggles
All data sources can be individually enabled/disabled via environment variables:
- `STOCK_PRICE`, `VNINDEX`, `GOLD_PRICE`, `EXCHANGE_RATE`, `CRYPTO_PRICE`

### Symbol Configuration
Symbols are comma-separated in environment variables (no spaces):
- `STOCK=VCB,TCB,VPB,MBB,VIC,HPG`
- `CRYPTO=BTC,ETH,BNB,USDT,DOGE,SOL`
- `EXCHANGE=USD` (can be multiple currencies)

## Telegram Integration

Uses `python-telegram-bot` library with async/await pattern. The bot:
- Sends a single combined message with all market data
- Uses Markdown formatting with code blocks for clean display
- Includes Vietnamese timezone (UTC+7) timestamps
- Handles errors gracefully without crashing the application

## GitHub Actions Deployment

Automated daily execution at 15:30 Vietnam time (08:30 UTC) via GitHub Actions workflow. Production environment variables are stored as GitHub secrets.

## Key Files for Development

- `main.py` - Application entry point and service orchestration
- `config/data_sources.py` - Add new symbols or enable/disable features
- `services/data_sources/` - Implement new market data sources
- `services/telegram/formatter.py` - Modify message formatting
- `.env.example` - Template for local configuration