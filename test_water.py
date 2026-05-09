# test_water.py
from experta import *
from knowledge_base.facts import FarmContext, WaterQuality, WaterAlert
from knowledge_base.water_rules import WaterQualityEngine

engine = WaterQualityEngine()
engine.reset()

# Simulate a stressed shrimp pond
engine.declare(FarmContext(species="shrimp"))
engine.declare(WaterQuality(
    ph          = 6.8,   # too low for shrimp
    ammonia     = 0.6,   # critical
    dissolved_o2= 3.5,   # warning
    temperature = 29.0,  # fine
    salinity    = 18.0,  # fine
))

engine.run()

print("\n── Water Alerts Fired ──")
for fact in engine.facts.values():
    if isinstance(fact, WaterAlert):
        print(f"\n  Parameter : {fact['parameter'].upper()}")
        print(f"  Level     : {fact['level'].upper()}")
        print(f"  Actual    : {fact['actual']}")
        print(f"  Safe Range: {fact['safe_range']}")
        print(f"  Correction: {fact['correction']}")