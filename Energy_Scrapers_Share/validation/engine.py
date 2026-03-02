"""
Validation Engine — main orchestrator.

Coordinates extractors, rules, and anomaly detection to produce
a complete validation report for a given date.
"""

import logging
from datetime import date
from typing import Any, Dict, List

from validation.extractors.iex_extractor import IEXExtractor
from validation.extractors.merit_extractor import MeritExtractor
from validation.extractors.coal_india_extractor import CoalIndiaExtractor
from validation.extractors.npp_extractor import NPPExtractor
from validation.extractors.ministry_coal_extractor import MinistryCoalExtractor
from validation.extractors.ministry_power_extractor import MinistryPowerExtractor

from validation.rules.generation_consistency import GenerationConsistencyRule
from validation.rules.coal_supply_vs_thermal import CoalSupplyVsThermalRule
from validation.rules.price_vs_demand import PriceVsDemandRule
from validation.rules.capacity_consistency import CapacityConsistencyRule
from validation.rules.renewable_plausibility import RenewablePlausibilityRule

from validation.anomaly import detect_anomalies
from validation.confidence import get_confidence

logger = logging.getLogger(__name__)

# ─── Registry ───────────────────────────────────────────────
EXTRACTORS = [
    IEXExtractor(),
    MeritExtractor(),
    CoalIndiaExtractor(),
    NPPExtractor(),
    MinistryCoalExtractor(),
    MinistryPowerExtractor(),
]

RULES = [
    GenerationConsistencyRule(),
    CoalSupplyVsThermalRule(),
    PriceVsDemandRule(),
    CapacityConsistencyRule(),
    RenewablePlausibilityRule(),
]


class ValidationEngine:
    """Orchestrates extraction, validation, and anomaly detection."""

    def __init__(self, target_date: date | None = None):
        self.target_date = target_date or date.today()
        self.metrics: List[Dict[str, Any]] = []
        self.validation_results: List[Dict[str, Any]] = []
        self.anomalies: List[Dict[str, Any]] = []

    def run(self) -> Dict[str, Any]:
        """Execute the full validation pipeline."""
        logger.info(f"═══ Validation Engine — {self.target_date} ═══")

        # Phase 1: Extract metrics from all sources
        logger.info("Phase 1: Extracting metrics...")
        self.metrics = self._extract_all()
        logger.info(f"  → Extracted {len(self.metrics)} metrics from {len(set(m['source'] for m in self.metrics))} sources")

        # Phase 2: Apply confidence scores
        for m in self.metrics:
            m["confidence"] = get_confidence(m["source"])

        # Phase 3: Run validation rules
        logger.info("Phase 2: Running validation rules...")
        self.validation_results = self._validate_all()
        logger.info(f"  → {len(self.validation_results)} validation checks completed")

        # Phase 4: Anomaly detection
        logger.info("Phase 3: Running anomaly detection...")
        self.anomalies = detect_anomalies(self.metrics)
        logger.info(f"  → {len(self.anomalies)} anomalies detected")

        # Build summary
        summary = self._build_summary()
        logger.info(f"═══ Validation Complete ═══")
        return summary

    def _extract_all(self) -> List[Dict[str, Any]]:
        """Run all extractors and collect metrics."""
        all_metrics: List[Dict[str, Any]] = []
        for extractor in EXTRACTORS:
            try:
                extracted = extractor.extract(self.target_date)
                all_metrics.extend(extracted)
                logger.info(f"  [{extractor.source_name}] {len(extracted)} metrics")
            except Exception as e:
                logger.error(f"  [{extractor.source_name}] Extraction failed: {e}")
        return all_metrics

    def _validate_all(self) -> List[Dict[str, Any]]:
        """Run all validation rules."""
        all_results: List[Dict[str, Any]] = []
        for rule in RULES:
            try:
                results = rule.validate(self.target_date, self.metrics)
                all_results.extend(results)
                statuses = [r["status"] for r in results]
                logger.info(
                    f"  [{rule.name}] {len(results)} checks "
                    f"(✅{statuses.count('pass')} ⚠{statuses.count('warn')} "
                    f"❗{statuses.count('fail')} ⏭{statuses.count('skip')})"
                )
            except Exception as e:
                logger.error(f"  [{rule.name}] Validation failed: {e}", exc_info=True)
        return all_results

    def _build_summary(self) -> Dict[str, Any]:
        """Build a summary dict of the validation run."""
        status_counts = {"pass": 0, "warn": 0, "fail": 0, "skip": 0}
        for r in self.validation_results:
            status_counts[r.get("status", "skip")] += 1

        anomaly_counts = {"info": 0, "warning": 0, "critical": 0}
        for a in self.anomalies:
            anomaly_counts[a.get("severity", "info")] += 1

        return {
            "date": self.target_date.isoformat(),
            "metrics_extracted": len(self.metrics),
            "sources_active": list(set(m["source"] for m in self.metrics)),
            "validation_checks": len(self.validation_results),
            "status_summary": status_counts,
            "anomalies_detected": len(self.anomalies),
            "anomaly_summary": anomaly_counts,
            "results": self.validation_results,
            "anomalies": self.anomalies,
            "metrics": self.metrics,
        }
