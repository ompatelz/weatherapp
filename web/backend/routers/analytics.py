"""Analytics router — correlation, intensity, and comparison endpoints."""

from __future__ import annotations

from typing import Optional
from async_lru import alru_cache

from fastapi import APIRouter, HTTPException, Query

from services.analytics_service import (
    calculate_energy_gdp_correlation,
    calculate_emissions_intensity,
    calculate_energy_intensity,
    compare_states,
    get_available_states,
    get_available_years_analytics,
    get_state_emissions,
    get_national_emissions_trend,
    get_emission_factors,
)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@alru_cache(maxsize=1)
async def get_cached_meta():
    return {
        "states": get_available_states(),
        "years": get_available_years_analytics(),
    }

@router.get("/meta")
async def analytics_meta():
    """Return available states and year range for analytics."""
    return await get_cached_meta()


@alru_cache(maxsize=32)
async def get_cached_correlation(year: int):
    return calculate_energy_gdp_correlation(year)

@router.get("/correlation")
async def correlation(
    year: Optional[int] = Query(default=None, description="Year for correlation analysis"),
):
    """Compute GDP-energy-emissions correlations for a given year."""
    if year is None:
        year = get_available_years_analytics()["max_year"]

    years_meta = get_available_years_analytics()
    if year < years_meta["min_year"] or year > years_meta["max_year"]:
        raise HTTPException(
            status_code=400,
            detail=f"Year must be between {years_meta['min_year']} and {years_meta['max_year']}"
        )

    return await get_cached_correlation(year)


@router.get("/emissions-intensity")
def emissions_intensity(
    year: Optional[int] = Query(default=None, description="Year for emissions intensity"),
):
    """Emissions per GDP for each state."""
    if year is None:
        year = get_available_years_analytics()["max_year"]

    return {
        "year": year,
        "data": calculate_emissions_intensity(year),
    }


@router.get("/energy-intensity")
def energy_intensity(
    year: Optional[int] = Query(default=None, description="Year for energy intensity"),
):
    """MW per billion INR GDP for each state."""
    if year is None:
        year = get_available_years_analytics()["max_year"]

    return {
        "year": year,
        "data": calculate_energy_intensity(year),
    }


@router.get("/compare")
def compare(
    states: str = Query(description="Comma-separated state IDs"),
    year: Optional[int] = Query(default=None, description="Year for comparison"),
):
    """Cross-state comparison for selected states."""
    state_ids = [s.strip() for s in states.split(",") if s.strip()]
    if len(state_ids) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 state IDs")

    if year is None:
        year = get_available_years_analytics()["max_year"]

    years_meta = get_available_years_analytics()
    if year < years_meta["min_year"] or year > years_meta["max_year"]:
        raise HTTPException(
            status_code=400,
            detail=f"Year must be between {years_meta['min_year']} and {years_meta['max_year']}"
        )

    return compare_states(state_ids, year)


@router.get("/emissions/state")
def state_emissions(
    year: Optional[int] = Query(default=None, description="Year for state emissions"),
):
    """Per-state CO₂ output, intensity, and year-on-year trend."""
    if year is None:
        year = get_available_years_analytics()["max_year"]
    return {"year": year, "data": get_state_emissions(year)}


@router.get("/emissions/trend")
def national_emissions_trend():
    """National CO₂ total aggregated by year."""
    return {"data": get_national_emissions_trend()}


@router.get("/emissions/factors")
def emission_factors():
    """IPCC emission factors (kg CO₂ / kWh) by fuel type."""
    return get_emission_factors()
