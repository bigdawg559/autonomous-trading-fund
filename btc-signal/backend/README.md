# BTC signal backend

From this directory:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn btc_signal.main:app --reload --port 8000
```

Worker:

```bash
python -m btc_signal.worker
```

Tests:

```bash
pytest -q
```
