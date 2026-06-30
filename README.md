# Autonomous Bitcoin Trading Fund System

A fully autonomous, self-learning quantitative trading platform with dynamic capital allocation, live execution on Binance, and real-time risk management.

## Features

✅ **Multi-Strategy Quant Engine** - Trend following, mean reversion, liquidity sweep, volatility breakout  
✅ **Dynamic Capital Allocator** - Weights strategies by Sharpe ratio, win rate, and consistency  
✅ **Live Execution** - Binance integration with position sizing and stop-loss enforcement  
✅ **Risk Management** - Kill switches, drawdown limits, max concurrent positions  
✅ **Feedback Loop** - Continuous performance tracking and weight rebalancing  
✅ **AI Reasoning** - OpenAI integration for trade explanations and market regime classification  
✅ **Backtesting & Simulation** - Monte Carlo simulations for strategy validation  
✅ **Real-time Dashboard** - Vercel UI displaying active strategies, allocations, PnL  

## Architecture

```
apps/
├── web/                    # Vercel dashboard
└── api/                    # API endpoints

services/
├── worker/                 # Market ingestion + signals
├── execution-engine/       # Live trading execution
├── strategy-engine/        # Multi-strategy system
├── allocator/              # Capital weight engine
├── ai-engine/              # OpenAI reasoning
└── risk-engine/            # Kill switches + limits

backtesting/
├── engine/                 # Backtesting framework
└── monte-carlo/            # MC simulations

supabase/
└── migrations/             # Database schema
```

## Quick Start

```bash
git clone https://github.com/bigdawg559/autonomous-trading-fund.git
cd autonomous-trading-fund
npm install
cp .env.example .env.local
npm run dev
```

## Deployment

See DEPLOYMENT.md for Vercel, Railway, and Supabase setup instructions.

## Trading Flow

```
Binance WebSocket → Worker → Strategy Engine → Allocator → 
Execution Engine → Risk Engine → Supabase → Dashboard
```

## Risk Management

- **Max Risk per Trade**: 2% of capital
- **Max Portfolio Drawdown**: -5% trigger kill switch
- **Max Concurrent Positions**: 5
- **All trades logged** for audit compliance

## Strategy Scoring

```
score = (sharpe_ratio * win_rate * consistency) - drawdown_penalty
weight = score / sum(all_scores)
```

⚠️ **TESTNET MODE ONLY** for initial deployments. Set `TRADING_ENABLED=false` in `.env`.
