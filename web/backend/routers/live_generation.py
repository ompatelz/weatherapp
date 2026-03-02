import json
import random
from fastapi import APIRouter, HTTPException
from services.mock_data import STATES_DATA

router = APIRouter()

@router.get("/live")
def get_live_generation():
    """
    Returns live (or simulated near-real-time) generation data 
    for all tracked states for the Map payload.
    """
    live_data = {}
    total_national_live = 0
    
    for state_id, state_info in STATES_DATA.items():
        # Get 2026 actual capacity as the realistic upper bounds
        cap_2026 = sum(state_info.get("capacity_by_year", {}).get(2026, {}).values())
        
        # In a real pipeline, this reads the Grid-India daily report payload that we'd write a scraper for. 
        # For this execution, we simulate based on actual capacity limits.
        
        if cap_2026 == 0:
            continue
            
        # Simulate current utilization factor (e.g. between 40% to 85% of total capacity is generating right now)
        utilization = random.uniform(0.40, 0.85)
        current_gen_mw = int(cap_2026 * utilization)
        total_national_live += current_gen_mw
        
        # Break it down proportionally to capacity mix but with random fluctuations 
        breakdown = state_info["capacity_by_year"][2026]
        gen_mix = {}
        for source, mw in breakdown.items():
            if mw > 0:
                # Solar only generates well during daytime, wind varies, thermal is steady baseline
                if source == 'solar':
                    source_util = random.uniform(0.1, 0.9)
                elif source == 'wind':
                    source_util = random.uniform(0.2, 0.7)
                else: 
                    source_util = random.uniform(0.6, 0.95)
                    
                val = int(mw * source_util)
                if val > 0:
                    gen_mix[source] = val
        
        # normalize to match actual total simulated gen so pies are accurate
        mix_sum = sum(gen_mix.values())
        if mix_sum > 0:
            gen_mix = {k: int((v/mix_sum)*current_gen_mw) for k,v in gen_mix.items()}
            
        live_data[state_id] = {
            "state_id": state_id,
            "state_name": state_info["name"],
            "current_generation_mw": current_gen_mw,
            "utilization_pct": round(utilization * 100, 1),
            "mix": gen_mix
        }
        
    return {
        "timestamp": "Live",
        "national_total_mw": total_national_live,
        "states": live_data
    }
