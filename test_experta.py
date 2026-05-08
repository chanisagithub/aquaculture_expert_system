# test_experta.py
# Purpose: Verify experta works correctly before building the real system

from experta import *

# ── 1. Define a simple Fact ───────────────────────────────────────────────────
class WaterReading(Fact):
    """Represents a single water quality reading from a pond."""
    parameter = Field(str, mandatory=True)   # e.g. "ph", "ammonia"
    value     = Field(float, mandatory=True)  # numeric reading
    species   = Field(str, mandatory=True)   # "tilapia" or "shrimp"


# ── 2. Define a simple KnowledgeEngine with a few rules ──────────────────────
class AquaTestEngine(KnowledgeEngine):

    # Rule fires when pH is dangerously low for tilapia
    @Rule(WaterReading(parameter="ph", value=MATCH.v, species="tilapia"),
          TEST(lambda v: v < 6.0))
    def tilapia_ph_critical_low(self, v):
        print(f"  [ALERT] Critical low pH detected: {v}")
        print(f"  [ACTION] Immediately apply agricultural lime (CaCO3) to raise pH.")

    # Rule fires when pH is in acceptable range for tilapia
    @Rule(WaterReading(parameter="ph", value=MATCH.v, species="tilapia"),
          TEST(lambda v: 6.5 <= v <= 8.5))
    def tilapia_ph_normal(self, v):
        print(f"  [OK] pH is within safe range for Tilapia: {v}")

    # Rule fires when ammonia is high for shrimp
    @Rule(WaterReading(parameter="ammonia", value=MATCH.v, species="shrimp"),
          TEST(lambda v: v > 0.5))
    def shrimp_ammonia_toxic(self, v):
        print(f"  [ALERT] Toxic ammonia level for shrimp: {v} mg/L")
        print(f"  [ACTION] Perform 30% water exchange. Reduce feeding immediately.")


# ── 3. Run the engine ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  Aquaculture Expert System — Experta Verification Test")
    print("=" * 55)

    engine = AquaTestEngine()
    engine.reset()  # Initializes working memory

    # Assert facts into working memory (simulating sensor input)
    print("\n>> Asserting Facts into Working Memory...")
    engine.declare(WaterReading(parameter="ph",      value=5.4,  species="tilapia"))
    engine.declare(WaterReading(parameter="ammonia", value=0.8,  species="shrimp"))
    engine.declare(WaterReading(parameter="ph",      value=7.2,  species="tilapia"))

    print("\n>> Running Inference Engine...\n")
    engine.run()  # Forward chaining fires all matching rules

    print("\n>> Working Memory Contents:")
    for fact_id, fact in engine.facts.items():
        print(f"   Fact #{fact_id}: {fact}")

    print("\n>> Test complete. Experta is working correctly.")
    print("=" * 55)
