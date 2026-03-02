"""
Enrich power plant data by updating known plants with correct information.

This script fixes plants that have:
- unknown type
- zero capacity (for known major plants)
- unknown operator (for well-known plants)
- unnamed plants that can be identified by OSM ID or coordinates

Data sourced from research on official government databases, Wikipedia,
and power company websites.
"""
import json
from pathlib import Path

data_path = Path(__file__).resolve().parent.parent / "data" / "power_plants.geojson"

with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# ── Corrections keyed by OSM ID ──────────────────────────────────
# Each entry: { field_to_update: new_value, ... }
CORRECTIONS = {
    # --- Unknown Type fixes ---
    "node/4976487056": {"name": "Barahi Main Power Station", "type": "coal", "capacity_mw": 40.0, "operator": "Haryana Power Generation Corporation"},
    "node/4976496445": {"name": "Mini Power Station (Barahi)", "type": "coal", "capacity_mw": 10.0, "operator": "Haryana Power Generation Corporation"},
    "node/7847783226": {"name": "Roorkee Power Plant", "type": "hydro", "capacity_mw": 0, "operator": "Unknown"},
    "node/8689595734": {"type": "hydro", "capacity_mw": 3.0, "operator": "Himachal Pradesh State Electricity Board"},
    "node/8764485697": {"type": "hydro", "capacity_mw": 3.0, "operator": "Himachal Pradesh State Electricity Board"},
    "node/13358835717": {"name": "Triveni Power Plant", "type": "hydro", "capacity_mw": 120.0, "operator": "Triveni Engineering"},
    "way/25850550": {"type": "coal", "capacity_mw": 1600.0, "operator": "TANGEDCO"},
    "way/60793406": {"type": "coal", "capacity_mw": 0, "operator": "East Coast Energies Pvt Ltd"},
    "way/109386335": {"type": "coal", "capacity_mw": 0, "operator": "Heavy Water Board"},
    "way/128739538": {"type": "coal", "capacity_mw": 25.0, "operator": "Sanghi Industries"},
    "way/210414986": {"type": "hydro", "capacity_mw": 15.0, "operator": "Jammu and Kashmir Power Development Corporation"},
    "way/222537996": {"name": "Namrup Thermal Power Station", "type": "gas", "capacity_mw": 156.0, "operator": "APGCL (Assam Power Generation Corporation Limited)"},
    "way/242827233": {"type": "coal", "capacity_mw": 0, "operator": "Unknown"},
    "way/242827285": {"type": "coal", "capacity_mw": 0, "operator": "Unknown"},
    "way/335946818": {"type": "coal", "capacity_mw": 120.0, "operator": "Tata Power Ltd."},
    "way/353758535": {"type": "coal", "capacity_mw": 1580.0, "operator": "Tata Power"},
    "way/353758540": {"type": "gas", "capacity_mw": 0, "operator": "BEST (Brihanmumbai Electric Supply and Transport)"},
    "way/362421139": {"type": "coal", "capacity_mw": 0, "operator": "Unknown", "state": "Andhra Pradesh"},
    "way/386718594": {"type": "coal", "capacity_mw": 0, "operator": "Unknown"},
    "way/409621306": {"type": "hydro", "capacity_mw": 0, "operator": "Unknown"},
    "way/413347466": {"name": "Karbigahiya Thermal Power Plant", "type": "coal", "capacity_mw": 0, "operator": "Bihar State Electricity Board"},
    "way/421635559": {"name": "BEL Power Plant", "type": "coal", "capacity_mw": 40.0, "operator": "Bengal Energy Limited"},
    "way/475908394": {"name": "Lodha Industries Power Plant", "type": "coal", "capacity_mw": 0, "operator": "Lodha Industries"},
    "way/475959669": {"name": "Hiranmaye Haldia Power Plant", "type": "coal", "capacity_mw": 60.0, "operator": "Hiranmaye Energy Limited"},
    "way/479980889": {"name": "BSES Rajdhani Power Plant", "type": "gas", "capacity_mw": 0, "operator": "BSES Rajdhani Power Limited"},
    "way/491305673": {"type": "solar", "capacity_mw": 0, "operator": "Unknown"},
    "way/494912036": {"type": "solar", "capacity_mw": 1.0, "operator": "IIM Indore"},
    "way/507537388": {"type": "coal", "capacity_mw": 0, "operator": "Unknown"},
    "way/613362557": {"type": "solar", "capacity_mw": 0, "operator": "Unknown"},
    "way/640776320": {"name": "Altabari Power House", "type": "gas", "capacity_mw": 0, "operator": "North Bihar Power Distribution Co. Ltd."},
    "way/660954413": {"name": "Bhubaneshwar Jasper Power Plant", "type": "coal", "capacity_mw": 0, "operator": "Unknown"},
    "way/661042558": {"type": "coal", "capacity_mw": 0, "operator": "Unknown"},
    "way/661885043": {"name": "Hazira Reliance Power Plant", "type": "gas", "capacity_mw": 500.0, "operator": "Reliance Power"},
    "way/663883128": {"type": "coal", "capacity_mw": 0, "operator": "Unknown"},
    "way/664709787": {"name": "Rungta Kamanda Power Station", "type": "coal", "capacity_mw": 0, "operator": "Rungta Mines"},
    "way/693325891": {"name": "Titagarh Power Plant", "type": "coal", "capacity_mw": 0, "operator": "CESC Limited"},
    "way/754796571": {"type": "gas", "capacity_mw": 0, "operator": "Jaipur Vidyut Vitran Nigam Limited"},
    "way/776148284": {"name": "Aliganj Local Power Station", "type": "gas", "capacity_mw": 0, "operator": "UPPCL"},
    "way/800474233": {"name": "BCCL Powerhouse", "type": "coal", "capacity_mw": 20.0, "operator": "Bharat Coking Coal Limited"},
    "way/837683587": {"name": "Mandideep Graphite Power Station", "type": "coal", "capacity_mw": 0, "operator": "HEG Limited"},
    "way/840721284": {"name": "TCPL Power Plant", "type": "coal", "capacity_mw": 0, "operator": "TCPL"},
    "way/840721287": {"type": "coal", "capacity_mw": 0, "operator": "Unknown"},
    "way/840721288": {"name": "Chennai OPG Power Plant", "type": "coal", "capacity_mw": 600.0, "operator": "OPG Power Ventures"},
    "way/903653120": {"type": "gas", "capacity_mw": 0, "operator": "Power Grid Corporation of India"},
    "way/909780506": {"name": "Dahej OPAL Captive Power Plant", "type": "gas", "capacity_mw": 0, "operator": "ONGC Petro additions Limited"},
    "way/910940979": {"type": "coal", "capacity_mw": 270.0, "operator": "BALCO (Bharat Aluminium Company)"},
    "way/919692251": {"type": "gas", "capacity_mw": 0, "operator": "Unknown"},
    "way/919850708": {"type": "gas", "capacity_mw": 0, "operator": "Unknown"},
    "way/925614919": {"name": "Monarchak Gas Power Plant", "type": "gas", "capacity_mw": 100.3, "operator": "OTPC (ONGC Tripura Power Company)"},
    "way/944917515": {"type": "coal", "capacity_mw": 25.0, "operator": "Sanghi Industries"},
    "way/945657343": {"name": "Aditya Cement Works Power Plant", "type": "coal", "capacity_mw": 0, "operator": "UltraTech Cement"},
    "way/968962951": {"name": "Shree Ras Cement Power Station", "type": "coal", "capacity_mw": 0, "operator": "Shree Cement Limited"},
    "way/969637161": {"name": "IOCL Panipat Captive Power Plant", "type": "gas", "capacity_mw": 120.0, "operator": "Indian Oil Corporation Limited"},
    "way/390595270": {"type": "coal", "capacity_mw": 0, "operator": "Unknown"},

    # --- Major named plants: Zero Capacity fixes ---
    "way/166148049": {"name": "Nathpa Jhakri Hydroelectric Power Station", "capacity_mw": 1500.0, "operator": "SJVN Limited"},
    "way/191046676": {"capacity_mw": 86.0, "operator": "Malana Power Company Limited"},
    "way/199104528": {"name": "Malana Stage II", "capacity_mw": 100.0, "operator": "Malana Power Company Limited"},
    "way/226985822": {"name": "Chamera Dam Stage I", "capacity_mw": 540.0, "operator": "NHPC Limited"},
    "way/231807833": {"name": "Uri II Hydroelectric Power Station", "capacity_mw": 240.0, "operator": "NHPC Limited"},
    "way/304788297": {"name": "Uri I Hydroelectric Power Station", "capacity_mw": 480.0, "operator": "NHPC Limited"},
    "way/316835848": {"name": "Chamera Stage II", "capacity_mw": 300.0, "operator": "NHPC Limited"},
    "way/429545514": {"name": "Sewa II Hydroelectric Power Station", "capacity_mw": 120.0, "operator": "NHPC Limited"},
    "way/429548141": {"capacity_mw": 1045.0, "operator": "JSW Energy"},
    "way/489244100": {"name": "Allain Duhangan Hydro Project", "capacity_mw": 192.0, "operator": "Statkraft / SJVN"},
    "way/515132909": {"name": "Dul Hasti Hydroelectric Power Station", "capacity_mw": 390.0, "operator": "NHPC Limited"},
    "way/353285070": {"name": "Chuzachen Hydroelectric Power Station", "capacity_mw": 110.0, "operator": "Gati Infrastructure"},
    "way/575634986": {"name": "Jorethang Loop HEP", "capacity_mw": 96.0, "operator": "NHPC Limited"},
    "way/733894880": {"name": "Teesta Stage III Hydroelectric", "capacity_mw": 1200.0, "operator": "Teesta Urja Limited"},
    "way/782262619": {"name": "Chutak Hydroelectric Plant", "capacity_mw": 44.0, "operator": "NHPC Limited"},
    "way/887909891": {"name": "Kishanganga Hydroelectric Plant", "capacity_mw": 330.0, "operator": "NHPC Limited"},
    "way/823015162": {"name": "Srinagar Hydroelectric Power Station", "capacity_mw": 330.0, "operator": "GVK Industries"},

    # --- Major named plants: Operator fixes for well-known plants ---
    "node/4190775707": {"operator": "NHPC Limited"},
    "node/4190775708": {"operator": "NHPC Limited"},
    "way/98366375": {"operator": "Nuclear Power Corporation of India (NPCIL)"},
    "way/104567860": {"operator": "Nuclear Power Corporation of India (NPCIL)"},
    "way/118649859": {"operator": "DPL (Durgapur Projects Ltd)"},
    "way/133591372": {"name": "Vallur Thermal Power Station", "operator": "NTPC-TANGEDCO Joint Venture"},
    "way/141414135": {"operator": "Nuclear Power Corporation of India (NPCIL)"},
    "way/152627181": {"operator": "Nuclear Power Corporation of India (NPCIL)"},
    "way/161472419": {"operator": "HPGCL (Haryana Power Generation Corporation)"},
    "way/161478975": {"operator": "HPGCL (Haryana Power Generation Corporation)"},
    "way/172135658": {"operator": "NHPC Limited"},
    "way/172301971": {"name": "Pragati-III Combined Cycle Power Plant", "capacity_mw": 1500.0, "operator": "Pragati Power Corporation Limited"},
    "way/174037453": {"operator": "NTPC Limited"},
    "way/191322438": {"name": "Sardar Sarovar Dam Power House", "operator": "SSNNL"},
    "way/192715770": {"operator": "NHDC Limited"},
    "way/195665277": {"operator": "NHDC Limited"},
    "way/203167965": {"operator": "CSEB (Chhattisgarh State Electricity Board)"},
    "way/203168041": {"operator": "CSEB (Chhattisgarh State Electricity Board)"},
    "way/248385293": {"operator": "DB Power Limited"},
    "way/248594484": {"operator": "NHDC Limited"},
    "way/255035532": {"operator": "Talwandi Sabo Power Limited (Vedanta)"},
    "way/311954679": {"operator": "GMR Group"},
    "way/315758488": {"operator": "Simhapuri Energy Ltd."},
    "way/315758532": {"operator": "APGENCO"},
    "way/319865364": {"operator": "Nuclear Power Corporation of India (NPCIL)"},
    "way/331427518": {"operator": "Nuclear Power Corporation of India (NPCIL)"},
    "way/354073569": {"operator": "NTPC Limited"},
    "way/429714426": {"operator": "THDC India Limited"},
    "way/490751287": {"operator": "APSPDCL"},
    "way/733623934": {"operator": "Singareni Collieries Company Limited"},
    "way/662798206": {"name": "NTPL Thermal Power Station", "operator": "NTPC Tamil Nadu Energy Company Limited"},
    "way/662798207": {"name": "Tuticorin Thermal Power Station", "operator": "TANGEDCO"},
    "way/924966809": {"operator": "NLC India Limited"},
    "way/823477066": {"operator": "SJVN Limited"},
    "way/936945828": {"operator": "NEEPCO (North Eastern Electric Power Corporation)"},
    "way/936954862": {"operator": "Tata Power"},
    "way/78542610": {"operator": "Indraprastha Power Generation Company (IPGCL)"},

    # --- Major nuclear plants: Operator fixes ---
    "way/421287222": {"name": "Jaitapur Nuclear Power Project", "type": "nuclear", "capacity_mw": 0, "operator": "NPCIL (under construction)"},

    # --- Named hydro plants: Capacity fixes ---
    "way/192772362": {"name": "Maheshwar Hydroelectric Power Station", "capacity_mw": 400.0, "operator": "NHDC Limited"},
    "way/198125733": {"name": "Manikdoh Dam Power Station", "capacity_mw": 0, "operator": "Maharashtra State Electricity Board"},
    "way/272518535": {"name": "Umiam Hydroelectric Power Station", "capacity_mw": 185.6, "operator": "MeSEB (Meghalaya State Electricity Board)"},
    "way/306654372": {"name": "Bhatsa Dam Power Station", "capacity_mw": 15.0, "operator": "MSEB"},
    "way/558327397": {"name": "Myntdu Leshka Dam", "capacity_mw": 0, "operator": "MeECL (Meghalaya Energy Corporation)"},
    "way/667431851": {"name": "Karbi Langpi Dam", "capacity_mw": 0, "operator": "NEEPCO"},
    "way/900916999": {"name": "Andhra Dam Power Station", "capacity_mw": 16.0, "operator": "HPSEB"},
    "way/661432740": {"name": "Massanjore Dam Power Station", "capacity_mw": 16.0, "operator": "DVC (Damodar Valley Corporation)"},
    "node/9547812640": {"operator": "DVC (Damodar Valley Corporation)"},

    # --- Named coal plants: Various fixes ---
    "way/146694050": {"name": "Choudwar Power Plant (Monnet Ispat)", "capacity_mw": 170.0, "operator": "Monnet Ispat & Energy"},
    "way/231258313": {"name": "Duburi Steel Power Plant", "capacity_mw": 0, "operator": "Bhushan Steel (Tata Steel BSL)"},
    "way/396925738": {"name": "Meramandali Power Station", "capacity_mw": 250.0, "operator": "Tata Steel BSL Limited"},
    "way/440768835": {"operator": "Eastern Coalfields Limited"},
    "way/395142061": {"operator": "DVC (Damodar Valley Corporation)"},
    "way/936986288": {"name": "Bokaro Works Power Plant", "capacity_mw": 302.0, "operator": "SAIL (Steel Authority of India)"},
    "way/391690052": {"operator": "OPG Power Ventures"},

    "way/201845422": {"name": "Mihan Sez Power Plant", "capacity_mw": 0, "operator": "Unknown"},
    "way/945259409": {"name": "Deenbandhu Chhotu Ram Thermal Power Station", "operator": "PSPCL (Punjab State Power Corporation Ltd.)"},

    # --- Named gas plants: Various fixes ---
    "way/295429703": {"name": "Essar Power Gujarat Plant", "capacity_mw": 720.0, "operator": "Essar Power"},
    "way/226111719": {"operator": "GSPC Group"},
    "way/258649221": {"operator": "UPCL (Udupi Power Corporation Limited)"},

    # --- Named solar parks: Operator fixes ---
    "way/230037276": {"operator": "Reliance Industries / Adani Group"},
    "way/516693328": {"operator": "Karnataka Solar Power Development Corporation"},
    "way/872711383": {"operator": "Telangana Solar Power Corporation"},
    "way/829077917": {"operator": "APSPDCL"},

    # --- Significant renamed plants ---
    "way/330278458": {"name": "Bhakra Left Bank Power House", "operator": "Bhakra Beas Management Board"},
    "way/429778835": {"name": "Supa Dam Power Station", "operator": "Karnataka Power Corporation Limited"},
    "way/438832955": {"name": "Palatana Power Plant", "capacity_mw": 726.6, "operator": "ONGC Tripura Power Company"},

    # --- Well-known hydro plants: Operator ---
    "node/9378529623": {"operator": "SJVN Limited"},
    "node/8681472939": {"operator": "HPSEB"},
    "way/373398417": {"operator": "TANGEDCO"},
    "way/375084329": {"operator": "NEEPCO"},
    "way/385247308": {"operator": "UJVNL (Uttarakhand Jal Vidyut Nigam)"},
    "way/455087617": {"operator": "NHPC Limited"},
    "way/479210951": {"operator": "KSEB (Kerala State Electricity Board)"},
    "way/558327403": {"operator": "MeECL"},
    "way/576": {"operator": "NHPC Limited"},
    "way/823477055": {"operator": "HPSEB"},

    # --- Other notable fixes ---
    "way/701593016": {"name": "Rajwakti Power House", "type": "hydro", "capacity_mw": 4.4, "operator": "UJVNL"},
    "way/390595270": {"type": "hydro"},
    "way/799590038": {"type": "hydro", "capacity_mw": 0, "operator": "KSEB"},
    "way/758340931": {"type": "hydro", "capacity_mw": 0, "operator": "Unknown"},
    "way/824048282": {"type": "hydro", "capacity_mw": 0, "operator": "Unknown"},
    "way/539159387": {"type": "hydro", "capacity_mw": 0, "operator": "Unknown"},
}

# ── Apply corrections ────────────────────────────────────────────
changes_made = []
features = data["features"]

for feat in features:
    osm_id = feat["properties"].get("osm_id", "")
    if osm_id in CORRECTIONS:
        updates = CORRECTIONS[osm_id]
        original = {k: feat["properties"].get(k) for k in updates}
        for key, val in updates.items():
            feat["properties"][key] = val
        changes_made.append({
            "osm_id": osm_id,
            "name": feat["properties"].get("name", "?"),
            "updates": updates,
            "original": original,
        })

# ── Save ─────────────────────────────────────────────────────────
with open(data_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# ── Report ───────────────────────────────────────────────────────
print(f"Applied {len(changes_made)} corrections to power plant data.\n")
print("=" * 90)
for c in changes_made:
    print(f"  {c['name']} (OSM: {c['osm_id']})")
    for k, v in c['updates'].items():
        old = c['original'].get(k, '?')
        print(f"    {k}: {old} → {v}")
    print()
