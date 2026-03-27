<div align="center">
  <img src=".github/banner.png" alt="moxchange banner" width="100%" />
</div>

<br />

<div align="center">

**A powerful backtesting simulator for automated and manual trading strategies.**  
Connect via WebSocket or REPL, replay historical OHLCV data, and stress-test your strategies with precision.

</div>

---

## Overview

moxchange lets you replay historical market data and interact with a simulated exchange in real time. Feed it a CSV of OHLCV data, spin up the server, and connect your bots or tools — then step through candles, place orders, manage your account, and pull detailed statistics.

It's designed to feel like a real exchange: your clients connect over WebSocket just like they would in production, so the gap between backtesting and live trading is as small as possible.

## Features

- **WebSocket API** — connect any number of clients simultaneously
- **REPL interface** — control the simulation interactively from your terminal
- **Step-through mode** — advance candle by candle for precise debugging
- **Order management** — place, modify, and cancel orders just like a real exchange
- **Account management** — track balances, positions, and P&L
- **Detailed statistics** — get a full breakdown of your strategy's performance

## Getting Started

**1. Prepare your data**

Format your historical market data as a CSV with OHLCV columns:

```
timestamp,open,high,low,close,volume
```

**2. Run moxchange**

```bash
moxchange your_data.csv
```

The WebSocket address will be printed to your terminal.

**3. Connect your client**

Point your trading bot or client at the displayed address and start backtesting.



## Contributing

This is my first serious open source project and I'm still growing as a developer — so if you spot a bug, a rough edge, or a way something could work better, please open an issue or pull request. All contributions are welcome.

**Something especially needed:** client libraries that wrap the WebSocket API into a clean, ergonomic interface — a Python one in particular would be fantastic. If that sounds like something you'd enjoy building, feel free to create a new repo and go for it. I'd be thrilled.

---

<div align="center">
  <sub>Built with 🤍 — PRs and issues welcome</sub>
</div> 