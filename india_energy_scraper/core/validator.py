import json
from pathlib import Path
from typing import List, Dict, Any
from core.schemas import StateEnergyData
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class Validator:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def cross_validate(self, all_records: List[StateEnergyData]) -> List[StateEnergyData]:
        # Simple reconciliation logic: group by state_id
        state_groups = {}
        for rec in all_records:
            state_groups.setdefault(rec.state_id, []).append(rec)
            
        reconciled = []
        discrepancies = []
        
        for state_id, records in state_groups.items():
            base = records[0].model_dump()
            source = records[0].provenance.source_url
            
            # Very basic demonstration of magnitude checks
            for r in records[1:]:
                # Check for large capability mismatch
                if r.total_capacity_mw and base.get("total_capacity_mw"):
                    diff = abs(r.total_capacity_mw - base["total_capacity_mw"]) / base["total_capacity_mw"]
                    if diff > 0.05:
                        discrepancies.append({
                            "state": state_id,
                            "field": "total_capacity_mw",
                            "sources": [source, r.provenance.source_url],
                            "values": [base["total_capacity_mw"], r.total_capacity_mw],
                            "diff_percent": diff * 100
                        })
                
                # Merge logic (prefer the first one arbitrarily for scaffolding, real logic goes here)
                pass
            
            reconciled.append(StateEnergyData(**base))
            
        self._write_report(discrepancies)
        return reconciled

    def _write_report(self, discrepancies: List[Dict]):
        report_path = self.output_dir / "cross_validation_report.md"
        with open(report_path, "w") as f:
            f.write("# Cross Validation Report\n\n")
            if not discrepancies:
                f.write("No major discrepancies found.\n")
            else:
                f.write("| State | Field | Sources | Values | Diff (%) |\n")
                f.write("|---|---|---|---|---|\n")
                for d in discrepancies:
                    sources = " vs ".join(d["sources"])
                    values = " vs ".join([str(x) for x in d["values"]])
                    f.write(f"| {d['state']} | {d['field']} | {sources} | {values} | {d['diff_percent']:.2f}% |\n")
                    
        logger.info(f"Cross validation report written to {report_path}")

    def generate_outputs(self, records: List[StateEnergyData]):
        # JSONL
        jsonl_path = self.output_dir / f"india_energy_atlas_combined_{pd.Timestamp.now().strftime('%Y%m%d')}.jsonl"
        with open(jsonl_path, "w") as f:
            for r in records:
                f.write(r.model_dump_json() + "\n")
                
        # Time series CSV
        ts_data = []
        for r in records:
            for trend in r.generation_trend:
                ts_data.append({
                    "state_id": r.state_id,
                    "state_name": r.state_name,
                    "period": trend.period,
                    "generation_gwh": trend.generation_gwh,
                    "capacity_mw": r.total_capacity_mw,
                    "provenance": r.provenance.source_url
                })
        
        if ts_data:
            df = pd.DataFrame(ts_data)
            csv_path = self.output_dir / f"india_energy_atlas_time_series_{pd.Timestamp.now().strftime('%Y%m%d')}.csv"
            df.to_csv(csv_path, index=False)
            
        # HTML dashboard
        html_path = self.output_dir / "verification_dashboard.html"
        with open(html_path, "w") as f:
            f.write(f"<html><body><h1>India Energy Atlas Verification</h1><p>Processed {len(records)} states.</p></body></html>")
            
        logger.info(f"Outputs generated in {self.output_dir}")
