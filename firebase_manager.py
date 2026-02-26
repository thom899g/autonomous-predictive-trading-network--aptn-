"""
Firebase Manager for APTN
Handles all Firestore operations with proper error handling and state management
"""
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore, exceptions
from google.cloud.firestore_v1.base_query import FieldFilter
from config import config

class FirebaseManager:
    """Manages Firebase Firestore operations for APTN"""
    
    def __init__(self):
        self.db = None
        self._initialize_firebase()
        
    def _initialize_firebase(self) -> None:
        """Initialize Firebase connection with error handling"""
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(config.firebase.credentials_path)
                firebase_admin.initialize_app(cred, {
                    'projectId': config.firebase.project_id
                })
            self.db = firestore.client()
            logging.info("Firebase Firestore initialized successfully")
        except FileNotFoundError as e:
            logging.error(f"Firebase credentials file not found: {e}")
            raise
        except exceptions.FirebaseError as e:
            logging.error(f"Firebase initialization error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error initializing Firebase: {e}")
            raise
    
    def save_market_data(self, symbol: str, timeframe: str, data: List[Dict[str, Any]]) -> bool:
        """
        Save market data to Firestore with timestamp-based organization
        
        Args:
            symbol: Trading symbol (e.g., BTC/USDT)
            timeframe: Chart timeframe (e.g., 1h, 4h, 1d)
            data: List of candlestick data dictionaries
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.db:
            logging.error("Firestore not initialized")
            return False
            
        try:
            collection_name = f"market_data_{symbol.replace('/', '_')}_{timeframe}"
            batch = self.db.b