# test_shrimp_disease.py
from experta import *
from knowledge_base.facts import (
    FarmContext, BehaviorSymptom, PhysicalSymptom,
    WaterAlert, DiseaseDiagnosis
)
from knowledge_base.disease_rules_shrimp import ShrimpDiseaseEngine

tests = [
    {
        "label"    : "Test 1: WSSV (High Confidence)",
        "behavior" : ["mass_mortality"],
        "physical" : [("shell_white_spots", "shell")],
        "alerts"   : []
    },
    {
        "label"    : "Test 2: EMS (High Confidence)",
        "behavior" : ["mass_mortality"],
        "physical" : [("empty_stomach", "body"), ("white_hepatopancreas", "body")],
        "alerts"   : []
    },
    {
        "label"    : "Test 3: Black Gill — Ammonia Linked",
        "behavior" : ["reduced_feeding"],
        "physical" : [("black_gills", "gill")],
        "alerts"   : [("ammonia", "critical", 0.8, "< 0.1 mg/L", "Water exchange")]
    },
    {
        "label"    : "Test 4: EHP / Running Mortality",
        "behavior" : ["whirling"],
        "physical" : [("white_muscle", "body")],
        "alerts"   : []
    },
]

for test in tests:
    print(f"\n{'='*55}")
    print(f"  {test['label']}")
    print(f"{'='*55}")

    engine = ShrimpDiseaseEngine()
    engine.reset()
    engine.declare(FarmContext(species="shrimp"))

    for b in test["behavior"]:
        engine.declare(BehaviorSymptom(symptom=b))

    for symptom, loc in test["physical"]:
        engine.declare(PhysicalSymptom(symptom=symptom, location=loc))

    for param, level, actual, safe, correction in test["alerts"]:
        engine.declare(WaterAlert(
            parameter=param, level=level,
            actual=actual, safe_range=safe, correction=correction
        ))

    engine.run()

    for fact in engine.facts.values():
        if isinstance(fact, DiseaseDiagnosis):
            print(f"  Disease   : {fact['disease']}")
            print(f"  Cause     : {fact['cause']}")
            print(f"  Confidence: {fact['confidence']}")
            print(f"  Urgency   : {fact['urgency']}")