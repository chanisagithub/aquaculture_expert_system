# Master orchestration engine
# Sequence:
#   1. Assert all input facts into shared working memory
#   2. Run WaterQualityEngine  → produces WaterAlert facts
#   3. Carry WaterAlert facts into disease engine working memory
#   4. Run species-specific DiseaseEngine → produces DiseaseDiagnosis facts
#   5. Deduplicate, sort by urgency, return structured output

from experta import Fact
from typing import Dict, List, Tuple
from knowledge_base.facts import (
    FarmContext, WaterQuality, BehaviorSymptom,
    PhysicalSymptom, WaterAlert, DiseaseDiagnosis
)
from knowledge_base.water_rules import WaterQualityEngine
from knowledge_base.disease_rules_tilapia import TilapiaDiseaseEngine
from knowledge_base.disease_rules_shrimp import ShrimpDiseaseEngine


# Urgency priority for sorting output
URGENCY_ORDER = {
    "Immediate"   : 0,
    "Within 24hrs": 1,
    "Monitor"     : 2,
    "Unknown"     : 3
}


def _extract_water_alerts(engine) -> List[Dict]:
    """Pull WaterAlert facts out of a finished engine's working memory."""
    alerts = []
    for fact in engine.facts.values():
        if isinstance(fact, WaterAlert):
            alerts.append({
                "parameter" : fact["parameter"],
                "level"     : fact["level"],
                "actual"    : fact["actual"],
                "safe_range": fact["safe_range"],
                "correction": fact["correction"]
            })
    return alerts


def _extract_diagnoses(engine) -> List[Dict]:
    """Pull DiseaseDiagnosis facts out of a finished engine's working memory."""
    diagnoses = []
    seen_diseases = set()  # deduplicate by disease name

    for fact in engine.facts.values():
        if isinstance(fact, DiseaseDiagnosis):
            name = fact["disease"]

            # If we've already added this disease, keep the higher confidence one
            if name in seen_diseases:
                continue

            # Skip the generic catch-all if real diagnoses were found
            if "Undetermined" in name and len(diagnoses) > 0:
                continue

            seen_diseases.add(name)
            diagnoses.append({
                "disease"   : name,
                "cause"     : fact["cause"],
                "confidence": fact["confidence"],
                "urgency"   : fact["urgency"],
                "treatment" : fact["treatment"],
                "prevention": fact["prevention"]
            })

    # Sort: Immediate first, then Within 24hrs, then Monitor
    diagnoses.sort(key=lambda d: URGENCY_ORDER.get(d["urgency"], 3))
    return diagnoses


def _deduplicate_alerts(alerts: List[Dict]) -> List[Dict]:
    """
    If both warning and critical fired for the same parameter,
    keep only critical (higher salience already fires first,
    but both get asserted — filter here).
    """
    seen = {}
    for alert in alerts:
        param = alert["parameter"]
        if param not in seen:
            seen[param] = alert
        else:
            # Keep whichever is more severe
            if alert["level"] == "critical":
                seen[param] = alert
    return list(seen.values())


def _build_farm_context(species, pond_age_days=None, stocking_density=None):
    """Create FarmContext without invalid None values for optional fields."""
    context = {"species": species}
    if pond_age_days is not None:
        context["pond_age_days"] = pond_age_days
    if stocking_density is not None:
        context["stocking_density"] = stocking_density
    return FarmContext(**context)


def run_full_diagnosis(
    species: str,
    water_params: Dict,
    behavior_symptoms: List[str],
    physical_symptoms: List[Tuple[str, str]],  # (symptom, location)
    pond_age_days: int = None,
    stocking_density: str = None
) -> Dict:
    """
    Main entry point called by the UI.

    Parameters
    ----------
    species             : "tilapia" or "shrimp"
    water_params        : dict of water readings e.g. {"ph": 7.2, "ammonia": 0.05}
    behavior_symptoms   : list of symptom strings e.g. ["lethargy", "surface_gasping"]
    physical_symptoms   : list of (symptom, location) tuples
    pond_age_days       : optional int
    stocking_density    : optional "low" | "medium" | "high"

    Returns
    -------
    dict with keys:
        "species"    : str
        "water_alerts"  : list of alert dicts
        "diagnoses"     : list of diagnosis dicts
        "overall_status": "Critical" | "Warning" | "Stable"
        "summary"       : str  — one-line plain-English summary
    """

    # ── PHASE 1: Water Quality Engine ────────────────────────────────────────
    water_engine = WaterQualityEngine()
    water_engine.reset()

    water_engine.declare(_build_farm_context(
        species, pond_age_days, stocking_density
    ))

    if water_params:
        water_engine.declare(WaterQuality(**water_params))

    water_engine.run()

    water_alerts = _deduplicate_alerts(_extract_water_alerts(water_engine))

    # ── PHASE 2: Disease Engine ───────────────────────────────────────────────
    DiseaseEngineClass = (
        TilapiaDiseaseEngine if species == "tilapia" else ShrimpDiseaseEngine
    )

    disease_engine = DiseaseEngineClass()
    disease_engine.reset()

    # Assert context
    disease_engine.declare(_build_farm_context(
        species, pond_age_days, stocking_density
    ))

    # Assert behavior symptoms
    for symptom in behavior_symptoms:
        disease_engine.declare(BehaviorSymptom(symptom=symptom))

    # Assert physical symptoms
    for symptom, location in physical_symptoms:
        disease_engine.declare(PhysicalSymptom(symptom=symptom, location=location))

    # ── KEY: Carry WaterAlert facts from Phase 1 into disease engine ──────────
    # This is what enables cross-domain reasoning
    for alert in water_alerts:
        disease_engine.declare(WaterAlert(**alert))

    disease_engine.run()

    diagnoses = _extract_diagnoses(disease_engine)

    # ── PHASE 3: Compute overall status ──────────────────────────────────────
    overall_status = _compute_overall_status(water_alerts, diagnoses)
    summary        = _build_summary(species, water_alerts, diagnoses, overall_status)

    return {
        "species"       : species,
        "water_alerts"  : water_alerts,
        "diagnoses"     : diagnoses,
        "overall_status": overall_status,
        "summary"       : summary
    }


def _compute_overall_status(alerts: List[Dict], diagnoses: List[Dict]) -> str:
    """
    Derive a single traffic-light status from all results.
    Critical water alert OR Immediate urgency disease → Critical
    Warning alert OR Within 24hrs disease             → Warning
    Everything else                                   → Stable
    """
    has_critical_alert    = any(a["level"] == "critical" for a in alerts)
    has_immediate_disease = any(d["urgency"] == "Immediate" for d in diagnoses)
    has_warning_alert     = any(a["level"] == "warning" for a in alerts)
    has_24hr_disease      = any(d["urgency"] == "Within 24hrs" for d in diagnoses)

    if has_critical_alert or has_immediate_disease:
        return "Critical"
    elif has_warning_alert or has_24hr_disease:
        return "Warning"
    else:
        return "Stable"


def _build_summary(species, alerts, diagnoses, status) -> str:
    """Build a one-line plain English summary for the UI header."""
    species_label = "Tilapia" if species == "tilapia" else "Shrimp"

    if status == "Stable":
        return f"{species_label} pond appears healthy. No critical issues detected."

    parts = []

    critical_params = [a["parameter"].upper() for a in alerts if a["level"] == "critical"]
    warning_params  = [a["parameter"].upper() for a in alerts if a["level"] == "warning"]

    if critical_params:
        parts.append(f"Critical water parameters: {', '.join(critical_params)}")
    if warning_params:
        parts.append(f"Warning water parameters: {', '.join(warning_params)}")

    immediate_diseases = [d["disease"] for d in diagnoses if d["urgency"] == "Immediate"]
    if immediate_diseases:
        parts.append(f"Immediate disease risk: {immediate_diseases[0]}")

    return f"{species_label} pond — {status}. " + ". ".join(parts) + "."
