from core.base_extractor import Extractor
from core.schemas import StateEnergyData, Provenance, GenerationTrend, EnergyMix
import logging
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import pdfplumber
import re

logger = logging.getLogger(__name__)

class NppExtractor(Extractor):
    def __init__(self, storage_root: str):
        super().__init__("npp.gov.in", storage_root)
        self.base_url = "https://npp.gov.in"
        self.published_reports_url = f"{self.base_url}/publishedReports"

    def discover(self):
        logger.info(f"Discovering reports at {self.published_reports_url}")
        urls = []
        try:
            response = self.client.get(self.published_reports_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/public-reports/' in href or href.endswith(('.pdf', '.xlsx', '.csv')):
                    full_url = href if href.startswith('http') else f"{self.base_url}{href}"
                    urls.append(full_url)
        except Exception as e:
            logger.error(f"Error discovering NPP reports: {e}")
        return list(set(urls))[:2]

    def download(self, url: str) -> str:
        logger.info(f"Downloading {url}")
        filename = url.split('/')[-1] or "index.html"
        today_date = datetime.now().strftime("%Y-%m-%d")
        ext = filename.split('.')[-1].lower()
        subfolder = "assets" if ext in ['pdf', 'xlsx', 'csv'] else "pages"
        out_dir = self.storage_root / today_date / subfolder
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / filename
        
        response = self.client.get(url, timeout=60.0)
        with open(out_path, 'wb') as f:
            f.write(response.content)
        return str(out_path)

    def parse(self, filepath: str):
        logger.info(f"Parsing {filepath}")
        records = []
        
        if filepath.endswith('.xlsx') or filepath.endswith('.csv'):
            try:
                df = pd.read_excel(filepath) if filepath.endswith('.xlsx') else pd.read_csv(filepath)
                header_idx = -1
                for idx, row in df.head(10).iterrows():
                    row_str = row.astype(str).str.lower().tolist()
                    if any("state" in s for s in row_str):
                        header_idx = idx
                        break
                
                if header_idx != -1:
                    df = pd.read_excel(filepath, header=header_idx) if filepath.endswith('.xlsx') else pd.read_csv(filepath, header=header_idx)
                    df.columns = df.columns.astype(str).str.lower().str.strip()
                    state_col = next((c for c in df.columns if "state" in c or "region" in c), None)

                    if state_col:
                        header_map = {
                            "solar": "solar_mw",
                            "wind": "wind_mw",
                            "hydro": "hydro_mw",
                            "bio": "biomass_mw",
                            "thermal": "coal_mw",
                            "nuclear": "nuclear_mw"
                        }
                        
                        source_cols = {}
                        for col in df.columns:
                            for key, target_field in header_map.items():
                                if key in col:
                                    source_cols[col] = target_field

                        if source_cols:
                            for _, row in df.iterrows():
                                state_name = row[state_col]
                                if pd.isna(state_name) or "total" in str(state_name).lower():
                                    continue

                                state_name = re.sub(r'^\d+\.?\s*', '', str(state_name)).strip()
                                
                                capacities = {"solar_mw": 0, "wind_mw": 0, "hydro_mw": 0, "biomass_mw": 0, "coal_mw": 0, "nuclear_mw": 0}
                                
                                for col, target_field in source_cols.items():
                                    val = row[col]
                                    try:
                                        val = float(val)
                                        if val > 0:
                                            capacities[target_field] += val
                                    except (ValueError, TypeError):
                                        continue

                                total_mw = sum(capacities.values())
                                if total_mw > 0:
                                    # State Mapping
                                    state_id = "".join([w[0].upper() for w in state_name.split()][:2])
                                    if len(state_id) < 2:
                                        state_id = state_name[:2].upper()
                                    state_map = {"Gujarat": "GJ", "Rajasthan": "RJ", "Karnataka": "KA", "Tamil Nadu": "TN", "Maharashtra": "MH"}
                                    if state_name in state_map:
                                        state_id = state_map[state_name]

                                    records.append({
                                        "state_id": state_id,
                                        "state_name": state_name,
                                        "total_capacity_mw": total_mw,
                                        "energy_mix": {
                                            "solar_percent": round((capacities["solar_mw"] / total_mw) * 100, 2) if total_mw else 0,
                                            "wind_percent": round((capacities["wind_mw"] / total_mw) * 100, 2) if total_mw else 0,
                                            "hydro_percent": round((capacities["hydro_mw"] / total_mw) * 100, 2) if total_mw else 0,
                                            "biomass_percent": round((capacities["biomass_mw"] / total_mw) * 100, 2) if total_mw else 0,
                                            "coal_percent": round((capacities["coal_mw"] / total_mw) * 100, 2) if total_mw else 0,
                                            "nuclear_percent": round((capacities["nuclear_mw"] / total_mw) * 100, 2) if total_mw else 0
                                        },
                                        "generation_trend": [],
                                        "provenance": {
                                            "source_url": self.published_reports_url,
                                            "download_timestamp": datetime.now().isoformat(),
                                            "file_path": filepath,
                                            "original_format": filepath.split('.')[-1],
                                            "extraction_method": "pandas-tabular",
                                            "confidence_score": 0.95,
                                            "preferred_source": {"total_capacity_mw": "NPP Report"}
                                        }
                                    })
            except Exception as e:
                logger.error(f"Failed to parse tabular data: {e}")

        # Return whatever we extracted
        return records
