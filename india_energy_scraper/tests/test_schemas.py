import pytest
from datetime import datetime
from core.schemas import StateEnergyData, Provenance, GenerationTrend

def test_valid_state_data():
    record = StateEnergyData(
        state_id="MH",
        state_name="Maharashtra",
        total_capacity_mw=45000.0,
        total_generation_gwh=120000.0,
        generation_trend=[
            GenerationTrend(period="2024-01", generation_gwh=8500.0)
        ],
        provenance=Provenance(
            source_url="https://mock.gov.in",
            download_timestamp=datetime.now(),
            file_path="/mock/path.csv",
            original_format="csv",
            extraction_method="pandas",
            confidence_score=0.95
        )
    )
    assert record.state_id == "MH"
    assert record.total_capacity_mw == 45000.0

def test_invalid_confidence_score():
    with pytest.raises(ValueError):
        Provenance(
            source_url="https://mock.gov.in",
            download_timestamp=datetime.now(),
            file_path="/mock/path.csv",
            original_format="csv",
            extraction_method="pandas",
            confidence_score=1.5  # Invalid, must be <= 1.0
        )
