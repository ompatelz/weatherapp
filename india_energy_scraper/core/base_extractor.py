from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pathlib import Path
from .schemas import StateEnergyData
from .utils import RateLimitedClient, setup_logger
import os

logger = setup_logger(__name__)

class Extractor(ABC):
    def __init__(self, domain: str, storage_root: str):
        self.domain = domain
        self.storage_root = Path(storage_root) / domain
        requests_per_second = float(os.environ.get("CONCURRENCY_PER_DOMAIN", 2.0))
        self.client = RateLimitedClient(requests_per_second=requests_per_second)
        
    @abstractmethod
    def discover(self) -> List[str]:
        """Discover URLs to process."""
        pass
        
    @abstractmethod
    def download(self, url: str) -> str:
        """Download remote asset to local storage."""
        pass
        
    @abstractmethod
    def parse(self, filepath: str) -> List[Dict[str, Any]]:
        """Parse local file to raw structured data."""
        pass
        
    def validate(self, records: List[Dict[str, Any]]) -> List[StateEnergyData]:
        """Validate raw dictionaries into Pydantic schema."""
        validated = []
        for rec in records:
            try:
                validated.append(StateEnergyData(**rec))
            except Exception as e:
                logger.error(f"Validation failed for record: {e}")
        return validated
