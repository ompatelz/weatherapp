from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class Provenance(BaseModel):
    source_url: str
    download_timestamp: datetime
    file_path: str
    original_format: str
    extraction_method: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    preferred_source: Optional[Dict[str, str]] = None

class EnergyMix(BaseModel):
    thermal_percent: Optional[float] = None
    coal_percent: Optional[float] = None
    gas_percent: Optional[float] = None
    lignite_percent: Optional[float] = None
    diesel_percent: Optional[float] = None
    solar_percent: Optional[float] = None
    wind_percent: Optional[float] = None
    hydro_percent: Optional[float] = None
    nuclear_percent: Optional[float] = None
    biomass_percent: Optional[float] = None
    other_percent: Optional[float] = None

class GenerationTrend(BaseModel):
    period: str  # YYYY-MM or YYYY
    generation_gwh: float
    period_type: str = "monthly" # monthly or annual

class StateEnergyData(BaseModel):
    state_id: str
    state_name: str
    total_capacity_mw: Optional[float] = None
    total_generation_gwh: Optional[float] = None
    energy_mix: Optional[EnergyMix] = None
    generation_trend: List[GenerationTrend] = []
    provenance: Provenance
