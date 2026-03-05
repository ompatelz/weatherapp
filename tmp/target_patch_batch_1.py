import json
from pathlib import Path

def target_enrich():
    data_path = Path(r"c:\Users\Om Patel\Videos\Projects\Energy Website\web\backend\data\power_plants.geojson")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Patch Map: Match by name (case-insensitive)
    patch_map = {
        "kadapa ultra mega solar park": {"capacity_mw": 1000, "operator": "Andhra Pradesh Solar Power Corporation"},
        "ananthapuramu ultra mega solar park": {"capacity_mw": 1500, "operator": "Andhra Pradesh Solar Power Corporation / NTPC"},
        "ananthapuramu-ii ultra mega solar park": {"capacity_mw": 500, "operator": "Andhra Pradesh Solar Power Corporation"},
        "ghatghar hydro power station": {"capacity_mw": 250, "operator": "MAHAGENCO"},
        "myntdu leshka dam": {"capacity_mw": 126, "operator": "Meghalaya Energy Corporation Limited"},
        "manikdoh dam power station": {"capacity_mw": 12, "operator": "MAHAGENCO"},
        "idamalayar hydroelectric power station": {"capacity_mw": 75, "operator": "Kerala State Electricity Board"},
        "middle kolab project": {"capacity_mw": 232, "operator": "Odisha Hydro Power Corporation"},
        "upper kolab hydro electric project": {"capacity_mw": 320, "operator": "Odisha Hydro Power Corporation"},
        "baira dam": {"capacity_mw": 180, "operator": "NHPC"},
        "karbi langpi power station": {"capacity_mw": 100, "operator": "APGCL"},
        "solang hydro power station": {"capacity_mw": 5, "operator": "SAIPL"},
        "thoothukudi ibtpl power station": {"capacity_mw": 1050, "operator": "Ind-Barath Thermal Power Ltd"}
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

    print(f"\nTargeted batch update complete. Patched {patched} major plants.")

if __name__ == "__main__":
    target_enrich()
