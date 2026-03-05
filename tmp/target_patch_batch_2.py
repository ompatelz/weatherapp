import json
from pathlib import Path

def target_enrich_v2():
    data_path = Path(r"c:\Users\Om Patel\Videos\Projects\Energy Website\web\backend\data\power_plants.geojson")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Patch Map: Match by name (case-insensitive)
    patch_map = {
        "welspun solar mp project bhagwanpura": {"capacity_mw": 151, "operator": "Welspun Energy"},
        "indravati dam": {"capacity_mw": 600, "operator": "Odisha Hydro Power Corporation"},
        "thenmala dam powerhouse": {"capacity_mw": 15, "operator": "Kerala State Electricity Board"},
        "jaitapur nuclear power project": {"capacity_mw": 10380, "operator": "Nuclear Power Corporation of India"},
        "roddam solar plant": {"capacity_mw": 50, "operator": "Multiple (Anantapur Ultra Mega Solar Park)"} # Using 50 as a placeholder for a single section if found
    }

    patched = 0
    for feature in data["features"]:
        name = feature["properties"].get("name", "").lower()
        if name in patch_map:
            p = patch_map[name]
            feature["properties"]["capacity_mw"] = p["capacity_mw"]
            feature["properties"]["operator"] = p["operator"]
            patched += 1
            print(f"Patched: {feature['properties']['name']} -> {p['capacity_mw']} MW")

    with open(data_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"\nTargeted batch update V2 complete. Patched {patched} major plants.")

if __name__ == "__main__":
    target_enrich_v2()
