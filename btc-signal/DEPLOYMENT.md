# Deployment

## Vercel

The dashboard is a Next.js application under `btc-signal/frontend`. The existing Vercel project linked to this repository is `autonomous-trading-fund-ai-engine`. Its project root must be configured to `btc-signal/frontend` before this dashboard can be deployed as the project root. This branch does not change the existing production project automatically.

## Railway

The worker is under `btc-signal/backend` and is intended to run persistently on Railway. Configure the service root/Dockerfile to `btc-signal/backend/Dockerfile` and start with `python -m btc_signal.worker`.

The connected Railway account currently has no active project and returned an expired-trial error when a project creation was attempted. Therefore no Railway deployment is claimed.
