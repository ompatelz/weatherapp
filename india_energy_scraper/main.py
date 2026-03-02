import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

from scrapers.npp_extractor import NppExtractor
from scrapers.mnre_extractor import MnreExtractor
from scrapers.grid_india_extractor import GridIndiaExtractor
from scrapers.iced_extractor import IcedExtractor
from core.validator import Validator

load_dotenv()

logging.basicConfig(level=getattr(logging, os.environ.get("LOG_LEVEL", "INFO")), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting India Energy Atlas Scraper...")
    storage_root = os.environ.get("STORAGE_ROOT", str(Path(__file__).parent / "data"))
    output_dir = str(Path(__file__).parent / "output")
    
    os.makedirs(storage_root, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    extractors = [
        NppExtractor(storage_root),
        MnreExtractor(storage_root),
        GridIndiaExtractor(storage_root),
        IcedExtractor(storage_root)
    ]
    
    all_validated_records = []
    
    for ext in extractors:
        urls = ext.discover()
        for url in urls:
            try:
                filepath = ext.download(url)
                raw_records = ext.parse(filepath)
                validated = ext.validate(raw_records)
                all_validated_records.extend(validated)
            except Exception as e:
                logger.error(f"Failed processing {url} with {ext.__class__.__name__}: {e}")
                
    validator = Validator(output_dir)
    final_records = validator.cross_validate(all_validated_records)
    validator.generate_outputs(final_records)
    
    logger.info("Scraping and validation completed.")

if __name__ == "__main__":
    main()
