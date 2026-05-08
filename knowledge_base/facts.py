# Covers: input facts (observations), intermediate facts, output facts

from experta import Fact, Field


# ════════════════════════════════════════════════════════════
#  INPUT FACTS — Asserted by the UI based on user input
# ════════════════════════════════════════════════════════════

class FarmContext(Fact):
    """
    Basic context about the farm session.
    Asserted once per diagnosis run.
    """
    species      = Field(str, mandatory=True)   # "tilapia" | "shrimp"
    pond_age_days = Field(int, mandatory=False)  # days since stocking
    stocking_density = Field(str, mandatory=False)  # "low" | "medium" | "high"


class WaterQuality(Fact):
    """
    Water parameter readings from the pond.
    All fields optional — system works with partial data.
    """
    ph          = Field(float, mandatory=False)   # 0–14
    ammonia     = Field(float, mandatory=False)   # mg/L (NH3)
    nitrite     = Field(float, mandatory=False)   # mg/L (NO2)
    dissolved_o2 = Field(float, mandatory=False)  # mg/L
    temperature = Field(float, mandatory=False)   # °C
    salinity    = Field(float, mandatory=False)   # ppt (shrimp only)
    turbidity   = Field(float, mandatory=False)   # NTU (shrimp only)


class BehaviorSymptom(Fact):
    """
    Observed behavioral symptom in fish/shrimp.
    One fact per symptom observed.
    """
    symptom = Field(str, mandatory=True)
    # Possible values:
    # "surface_gasping"     – crowding at surface, gulping air
    # "erratic_swimming"    – darting, spiral, loss of balance
    # "lethargy"            – sitting at bottom, unresponsive
    # "flashing"            – rubbing/scratching against surfaces
    # "reduced_feeding"     – ignoring feed
    # "mass_mortality"      – sudden deaths in large numbers
    # "whirling"            – spinning in circles (shrimp)
    # "near_inlet_crowding" – all fish near water inlet


class PhysicalSymptom(Fact):
    """
    Observed physical/visual symptom on the body.
    One fact per symptom observed.
    """
    symptom  = Field(str, mandatory=True)
    location = Field(str, mandatory=False)  # "body" | "fin" | "gill" | "eye" | "shell"
    # Possible symptom values:
    # "hemorrhagic_ulcer"      – bloody open sores
    # "white_spots"            – salt-grain white dots
    # "white_patches"          – larger cloudy areas
    # "cotton_growth"          – fluffy fungal appearance
    # "fin_erosion"            – frayed/rotting fins
    # "pop_eye"                – exophthalmia, bulging eye
    # "body_darkening"         – overall dark discoloration
    # "red_discoloration"      – redness on body/legs (shrimp)
    # "black_gills"            – dark gill coloration
    # "white_muscle"           – muscle turning white (shrimp)
    # "soft_shell"             – shell not hardening (shrimp)
    # "white_hepatopancreas"   – pale/white digestive gland (shrimp)
    # "empty_stomach"          – transparent/empty gut (shrimp)
    # "shell_white_spots"      – white spots visible under shell


# ════════════════════════════════════════════════════════════
#  INTERMEDIATE FACTS — Asserted by water quality sub-engine
#  These feed INTO the disease diagnosis engine
# ════════════════════════════════════════════════════════════

class WaterAlert(Fact):
    """
    Fired by water rules when a parameter is out of range.
    Can contribute to disease diagnosis (e.g. low O2 → stress symptoms)
    """
    parameter  = Field(str, mandatory=True)   # "ph" | "ammonia" | "dissolved_o2" etc.
    level      = Field(str, mandatory=True)   # "warning" | "critical"
    actual     = Field(float, mandatory=True) # the actual measured value
    safe_range = Field(str, mandatory=True)   # human readable e.g. "6.5 – 8.5"
    correction = Field(str, mandatory=True)   # what to do


# ════════════════════════════════════════════════════════════
#  OUTPUT FACTS — Asserted by disease engine as conclusions
# ════════════════════════════════════════════════════════════

class DiseaseDiagnosis(Fact):
    """
    A disease conclusion fired by the diagnosis engine.
    Multiple may be asserted if symptoms overlap.
    """
    disease      = Field(str, mandatory=True)
    cause        = Field(str, mandatory=True)   # "Bacterial" | "Viral" | "Parasitic" | "Fungal" | "Environmental"
    confidence   = Field(str, mandatory=True)   # "High" | "Medium" | "Low"
    treatment    = Field(str, mandatory=True)
    prevention   = Field(str, mandatory=True)
    urgency      = Field(str, mandatory=True)   # "Immediate" | "Within 24hrs" | "Monitor"


class SystemConclusion(Fact):
    """
    Final overall conclusion asserted after all rules fire.
    Summarizes severity of the situation.
    """
    overall_status = Field(str, mandatory=True)  # "Critical" | "Warning" | "Stable"
    primary_issue  = Field(str, mandatory=True)
    action_summary = Field(str, mandatory=True)