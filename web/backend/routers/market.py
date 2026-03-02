from fastapi import APIRouter
from typing import Dict, List
from pydantic import BaseModel
import random

router = APIRouter()

class MarketPrice(BaseModel):
    state_id: str
    price_inr_per_mwh: float
    status: str

class LiveMarketResponse(BaseModel):
    timestamp: str
    prices: List[MarketPrice]

@router.get("/pricing/live", response_model=LiveMarketResponse)
def get_live_market_pricing():
    """
    Simulates fetching Day-Ahead Market (DAM) clearing prices from the Indian Energy Exchange (IEX).
    In production, this would query a database populated by the `IexExtractor`.
    """
    states = [
        "AP", "AR", "AS", "BR", "CT", "GA", "GJ", "HR", "HP", "JH", 
        "KA", "KL", "KL", "MP", "MH", "MN", "ML", "MZ", "MZ", "NL", 
        "OR", "PB", "RJ", "SK", "TN", "TG", "TR", "UP", "UT", "WB"
    ]
    
    # Base price around ~₹4000/MWh. Add some randomness.
    prices = []
    for state in set(states):
        base = 3500 + random.random() * 2000
        # Give some states typically higher prices
        if state in ["MH", "UP", "HR"]:
            base += 1000
        elif state in ["GJ", "TN", "KA"]: # High RE states
            base -= 500
        
        status = "normal"
        if base > 5000:
            status = "high"
        elif base < 3500:
            status = "low"
            
        prices.append(MarketPrice(
            state_id=state,
            price_inr_per_mwh=round(base, 2),
            status=status
        ))
        
    return LiveMarketResponse(
        timestamp="2026-02-28T12:00:00Z",
        prices=prices
    )
