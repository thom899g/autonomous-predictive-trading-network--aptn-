"""
APTN Configuration Module
Centralized configuration management with environment variable support
"""
import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from dotenv import load_dotenv
import logging

load_dotenv()

@dataclass
class ExchangeConfig:
    """Exchange API configuration"""
    name: str = "binance"
    api_key: str = os.getenv("EXCHANGE_API_KEY", "")
    api_secret: str = os.getenv("EXCHANGE_API_SECRET", "")
    testnet: bool = os.getenv("EXCHANGE_TESTNET", "true").lower() == "true"
    rate_limit: int = 1200  # requests per minute
    
@dataclass
class FirebaseConfig:
    """Firebase configuration for state management"""
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "")
    credentials_path: str = os.getenv("FIREBASE_CREDENTIALS", "serviceAccountKey.json")
    
@dataclass
class ModelConfig:
    """Deep learning model configuration"""
    sequence_length: int = 60
    prediction_horizon: int = 5
    lstm_units: List[int] = (64, 32)
    dropout_rate: float = 0.2
    learning_rate: float = 0.001
    batch_size: int = 32
    epochs: int = 100
    validation_split: float = 0.2
    
@dataclass
class TradingConfig:
    """Trading strategy configuration"""
    symbols: List[str] = ("BTC/USDT", "ETH/USDT", "SOL/USDT")
    timeframe: str = "1h"
    initial_capital: float = 10000.0
    max_position_size: float = 0.1  # 10% of capital per trade
    stop_loss_pct: float = 0.02  # 2% stop loss
    take_profit_pct: float = 0.04  # 4% take profit
    confidence_threshold: float = 0.65  # Minimum model confidence
    
@dataclass
class APTNConfig:
    """Main APTN configuration"""
    exchange: ExchangeConfig = ExchangeConfig()
    firebase: FirebaseConfig = FirebaseConfig()
    model: ModelConfig = ModelConfig()
    trading: TradingConfig = TradingConfig()
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    telegram_bot_token: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")
    
    def validate(self) -> bool:
        """Validate critical configuration"""
        if not self.exchange.api_key or not self.exchange.api_secret:
            logging.error("Exchange API credentials not configured")
            return False
        if not self.firebase.project_id:
            logging.error("Firebase project ID not configured")
            return False
        return True

# Global configuration instance
config = APTNConfig()