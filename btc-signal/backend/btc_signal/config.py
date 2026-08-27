from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    database_url: str = 'sqlite:///./btc_signal.db'
    binance_rest_url: str = 'https://api.binance.com'
    binance_ws_url: str = 'wss://stream.binance.com:9443/ws'
    symbol: str = 'BTCUSDT'
    timeframe: str = '15m'
    stale_after_seconds: int = 120
    environment: str = 'local'
    log_level: str = 'INFO'


settings = Settings()
