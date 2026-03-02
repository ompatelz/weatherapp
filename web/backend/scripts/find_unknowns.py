"""Find power plants with missing or unknown data and write results to file."""
import json
from pathlib import Path

data_path = Path(__file__).resolve().parent.parent / "data" / "power_plants.geojson"
out_path = Path(__file__).resolve().parent / "unknowns_output.txt"

with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

features = data["features"]
lines = []
lines.append(f"Total plants: {len(features)}")

unknowns = []
for feat in features:
    p = feat["properties"]
    issues = []
    if p.get("type", "") in ("unknown", ""):
        issues.append("unknown_type")
    if p.get("capacity_mw", 0) == 0:
        issues.append("zero_capacity")
    if p.get("operator", "") in ("Unknown", ""):
        issues.append("unknown_operator")
    if "Unnamed" in p.get("name", "") or p.get("name", "") == "":
        issues.append("unnamed")
    if issues:
        unknowns.append({"properties": p, "issues": issues, "geometry": feat.get("geometry", {})})

lines.append(f"Plants with issues: {len(unknowns)}")
lines.append("---")
for item in unknowns:
    p = item["properties"]
    coords = item.get("geometry", {}).get("coordinates", [])
    lines.append(f"Name: {p.get('name','?')} | Type: {p.get('type','?')} | Capacity: {p.get('capacity_mw',0)} MW | Operator: {p.get('operator','?')} | State: {p.get('state','?')} | OSM: {p.get('osm_id','?')} | Coords: {coords} | Issues: {item['issues']}")

with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"Written {len(unknowns)} entries to {out_path}")
