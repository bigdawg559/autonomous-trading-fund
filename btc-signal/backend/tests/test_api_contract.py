REQUIRED_ENDPOINTS = {
    '/health',
    '/api/market/btcusdt',
    '/api/candles/btcusdt/15m',
    '/api/signal/current',
    '/api/system/status',
}


def test_required_endpoint_set():
    assert '/api/signal/current' in REQUIRED_ENDPOINTS
