# test_master.py
# Tests the complete pipeline: water engine → disease engine → structured output

from engine.master_engine import run_full_diagnosis
import json

print("\n" + "="*60)
print("  MASTER ENGINE — End-to-End Pipeline Tests")
print("="*60)


# ── Scenario 1: Shrimp pond — WSSV + bad water ───────────────────────────────
print("\n📍 Scenario 1: Shrimp pond — WSSV suspected + critical ammonia")
result = run_full_diagnosis(
    species            = "shrimp",
    water_params       = {"ph": 7.0, "ammonia": 0.7, "dissolved_o2": 3.2,
                          "temperature": 29.0, "salinity": 18.0},
    behavior_symptoms  = ["mass_mortality"],
    physical_symptoms  = [("shell_white_spots", "shell")]
)

print(f"\n  Overall Status : {result['overall_status']}")
print(f"  Summary        : {result['summary']}")
print(f"\n  Water Alerts ({len(result['water_alerts'])}):")
for a in result["water_alerts"]:
    print(f"    [{a['level'].upper()}] {a['parameter'].upper()} = {a['actual']}")
print(f"\n  Diagnoses ({len(result['diagnoses'])}):")
for d in result["diagnoses"]:
    print(f"    [{d['urgency']}] {d['disease']} ({d['confidence']} confidence)")


# ── Scenario 2: Tilapia pond — Streptococcosis ───────────────────────────────
print("\n" + "-"*60)
print("📍 Scenario 2: Tilapia pond — Streptococcosis + mild water issues")
result2 = run_full_diagnosis(
    species            = "tilapia",
    water_params       = {"ph": 7.8, "ammonia": 0.05, "dissolved_o2": 4.2,
                          "temperature": 28.0},
    behavior_symptoms  = ["erratic_swimming", "lethargy"],
    physical_symptoms  = [("pop_eye", "eye"), ("body_darkening", "body")]
)

print(f"\n  Overall Status : {result2['overall_status']}")
print(f"  Summary        : {result2['summary']}")
print(f"\n  Water Alerts ({len(result2['water_alerts'])}):")
for a in result2["water_alerts"]:
    print(f"    [{a['level'].upper()}] {a['parameter'].upper()} = {a['actual']}")
print(f"\n  Diagnoses ({len(result2['diagnoses'])}):")
for d in result2["diagnoses"]:
    print(f"    [{d['urgency']}] {d['disease']} ({d['confidence']} confidence)")


# ── Scenario 3: Healthy pond — no issues ─────────────────────────────────────
print("\n" + "-"*60)
print("📍 Scenario 3: Healthy tilapia pond — all parameters in range")
result3 = run_full_diagnosis(
    species            = "tilapia",
    water_params       = {"ph": 7.2, "ammonia": 0.01, "dissolved_o2": 6.5,
                          "temperature": 27.0, "nitrite": 0.05},
    behavior_symptoms  = [],
    physical_symptoms  = []
)

print(f"\n  Overall Status : {result3['overall_status']}")
print(f"  Summary        : {result3['summary']}")
print(f"  Water Alerts   : {len(result3['water_alerts'])}")
print(f"  Diagnoses      : {len(result3['diagnoses'])}")