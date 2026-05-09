# test_tilapia_disease.py
from experta import *
from knowledge_base.facts import (
    FarmContext, BehaviorSymptom, PhysicalSymptom,
    WaterAlert, DiseaseDiagnosis
)
# from knowledge_base.water_rules import WaterQualityEngine
from knowledge_base.disease_rules_tilapia import TilapiaDiseaseEngine

print("=" * 60)
print("  Scenario: Tilapia pond with ulcers, fin rot, and lethargy")
print("=" * 60)

# ── Test 1: MAS (High Confidence) ────────────────────────────
engine = TilapiaDiseaseEngine()
engine.reset()
engine.declare(FarmContext(species="tilapia"))
engine.declare(BehaviorSymptom(symptom="lethargy"))
engine.declare(PhysicalSymptom(symptom="hemorrhagic_ulcer", location="body"))
engine.declare(PhysicalSymptom(symptom="fin_erosion", location="fin"))
engine.run()

print("\n── Test 1: MAS Diagnosis ──")
for fact in engine.facts.values():
    if isinstance(fact, DiseaseDiagnosis):
        print(f"  Disease   : {fact['disease']}")
        print(f"  Confidence: {fact['confidence']}")
        print(f"  Urgency   : {fact['urgency']}")
        print(f"  Treatment :\n{fact['treatment']}")

# ── Test 2: Streptococcosis (High Confidence) ─────────────────
engine2 = TilapiaDiseaseEngine()
engine2.reset()
engine2.declare(FarmContext(species="tilapia"))
engine2.declare(PhysicalSymptom(symptom="pop_eye", location="eye"))
engine2.declare(BehaviorSymptom(symptom="erratic_swimming"))
engine2.declare(PhysicalSymptom(symptom="body_darkening", location="body"))
engine2.run()

print("\n── Test 2: Streptococcosis Diagnosis ──")
for fact in engine2.facts.values():
    if isinstance(fact, DiseaseDiagnosis):
        print(f"  Disease   : {fact['disease']}")
        print(f"  Confidence: {fact['confidence']}")
        print(f"  Urgency   : {fact['urgency']}")

# ── Test 3: Nitrite poisoning cross-referencing WaterAlert ────
engine3 = TilapiaDiseaseEngine()
engine3.reset()
engine3.declare(FarmContext(species="tilapia"))
engine3.declare(WaterAlert(
    parameter="nitrite", level="critical",
    actual=0.7, safe_range="< 0.1 mg/L",
    correction="Perform water exchange"
))
engine3.declare(BehaviorSymptom(symptom="lethargy"))
engine3.run()

print("\n── Test 3: Nitrite Poisoning (WaterAlert cross-reference) ──")
for fact in engine3.facts.values():
    if isinstance(fact, DiseaseDiagnosis):
        print(f"  Disease   : {fact['disease']}")
        print(f"  Confidence: {fact['confidence']}")
        print(f"  Urgency   : {fact['urgency']}")