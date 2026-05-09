# Disease Diagnosis Rules — Tilapia (Oreochromis niloticus)
#
# Diseases covered:
#   1. Motile Aeromonas Septicemia (MAS)
#   2. Columnaris Disease
#   3. Streptococcosis
#   4. Ichthyophthirius (White Spot / Ich)
#   5. Saprolegniasis (Fungal)
#   6. Environmental Oxygen Stress
#   7. Nitrite Poisoning (Brown Blood Disease)
#
# Rule matching strategy:
#   - Primary symptoms    → High confidence
#   - Partial symptoms    → Medium confidence
#   - Water alert only    → Low confidence (environmental suspicion)
#
# Salience:
#   20 = high confidence diagnosis (multiple strong symptom matches)
#   10 = medium confidence diagnosis
#    5 = low confidence / single indicator

from experta import KnowledgeEngine, Rule, MATCH, OR, NOT
from knowledge_base.facts import (
    FarmContext, BehaviorSymptom, PhysicalSymptom, WaterAlert, DiseaseDiagnosis
)


class TilapiaDiseaseEngine(KnowledgeEngine):

    # ════════════════════════════════════════════════════════
    #  DISEASE 1: Motile Aeromonas Septicemia (MAS)
    #  Cause   : Aeromonas hydrophila (Bacterial)
    #  Trigger : Poor water quality + physical trauma + stress
    #  Hallmark: Hemorrhagic ulcers + fin rot + bloating
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="tilapia"),
        BehaviorSymptom(symptom="lethargy"),
        PhysicalSymptom(symptom="hemorrhagic_ulcer"),
        PhysicalSymptom(symptom="fin_erosion"),
        salience=20
    )
    def tilapia_mas_high_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Motile Aeromonas Septicemia (MAS)",
            cause      = "Bacterial — Aeromonas hydrophila",
            confidence = "High",
            urgency    = "Immediate",
            treatment  = (
                "1. Isolate visibly infected fish immediately.\n"
                "2. Bath treatment: Oxytetracycline at 50–75 mg/L for 1 hour.\n"
                "3. Feed medicated pellets with Oxytetracycline (55 mg/kg feed) "
                "for 10 days if fish are still eating.\n"
                "4. Apply salt bath (3–5 g/L NaCl) for 5–10 minutes to reduce "
                "secondary infections.\n"
                "5. Perform 30% water exchange and improve aeration.\n"
                "6. Contact a licensed vet for antibiotic prescription in Sri Lanka."
            ),
            prevention = (
                "Maintain ammonia < 0.02 mg/L. Avoid sharp temperature swings. "
                "Do not overstock. Handle fish carefully to prevent skin damage "
                "which is the primary entry point for Aeromonas."
            )
        ))

    @Rule(
        FarmContext(species="tilapia"),
        PhysicalSymptom(symptom="hemorrhagic_ulcer"),
        NOT(PhysicalSymptom(symptom="fin_erosion")),
        salience=10
    )
    def tilapia_mas_medium_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Motile Aeromonas Septicemia (MAS) — Suspected",
            cause      = "Bacterial — Aeromonas hydrophila",
            confidence = "Medium",
            urgency    = "Within 24hrs",
            treatment  = (
                "Monitor closely for fin erosion and bloating. "
                "Perform 25% water exchange. Improve aeration. "
                "If symptoms worsen within 24 hours, begin Oxytetracycline treatment."
            ),
            prevention = (
                "Check ammonia and nitrite levels. "
                "Reduce stocking density if overcrowded."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  DISEASE 2: Columnaris Disease
    #  Cause   : Flavobacterium columnare (Bacterial)
    #  Trigger : High temperature + low oxygen + stress
    #  Hallmark: Saddle-shaped white patch near dorsal fin
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="tilapia"),
        PhysicalSymptom(symptom="white_patches", location="body"),
        PhysicalSymptom(symptom="fin_erosion"),
        BehaviorSymptom(symptom="lethargy"),
        salience=20
    )
    def tilapia_columnaris_high_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Columnaris Disease (Saddleback Disease)",
            cause      = "Bacterial — Flavobacterium columnare",
            confidence = "High",
            urgency    = "Immediate",
            treatment  = (
                "1. Bath treatment: Potassium permanganate (KMnO₄) at 2–3 mg/L "
                "for 1 hour — DO NOT exceed this concentration, it is toxic at higher doses.\n"
                "2. Alternatively: Copper sulfate at 0.5 mg/L for 1 hour.\n"
                "3. Salt treatment: 10 g/L NaCl for 30 minutes.\n"
                "4. If systemic (fish not eating): consult vet for Florfenicol-medicated feed.\n"
                "5. Lower water temperature if above 30°C — Columnaris thrives in heat."
            ),
            prevention = (
                "Keep dissolved O₂ above 5 mg/L. "
                "Columnaris spreads rapidly in warm low-oxygen conditions. "
                "Common during Sri Lanka's dry season (April–September) "
                "when pond temperatures peak."
            )
        ))

    @Rule(
        FarmContext(species="tilapia"),
        PhysicalSymptom(symptom="white_patches", location="body"),
        NOT(PhysicalSymptom(symptom="fin_erosion")),
        salience=10
    )
    def tilapia_columnaris_medium_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Columnaris Disease — Suspected",
            cause      = "Bacterial — Flavobacterium columnare",
            confidence = "Medium",
            urgency    = "Within 24hrs",
            treatment  = (
                "Apply salt bath (5 g/L) as precaution. Monitor for fin erosion. "
                "Check water temperature — reduce if above 30°C."
            ),
            prevention = (
                "Increase aeration. Avoid handling fish during hot weather."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  DISEASE 3: Streptococcosis
    #  Cause   : Streptococcus agalactiae (Bacterial)
    #  Trigger : High density + high temperature
    #  Hallmark: Pop-eye (exophthalmia) + spiral swimming + darkening
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="tilapia"),
        PhysicalSymptom(symptom="pop_eye"),
        BehaviorSymptom(symptom="erratic_swimming"),
        PhysicalSymptom(symptom="body_darkening"),
        salience=20
    )
    def tilapia_streptococcosis_high_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Streptococcosis",
            cause      = "Bacterial — Streptococcus agalactiae",
            confidence = "High",
            urgency    = "Immediate",
            treatment  = (
                "1. Medicated feed: Erythromycin at 100 mg/kg feed for 14 days "
                "(prescription required in Sri Lanka).\n"
                "2. Remove and destroy all dead fish immediately — Streptococcus "
                "spreads through cannibalism of dead fish.\n"
                "3. Reduce stocking density if possible.\n"
                "4. Perform 30–40% water exchange.\n"
                "5. NOTE: Streptococcosis is a zoonotic risk — "
                "wash hands thoroughly after handling infected fish."
            ),
            prevention = (
                "Streptococcosis is the most economically damaging tilapia disease "
                "in Sri Lanka. Use certified pathogen-free fingerlings from NARA or NAQDA. "
                "Avoid stocking density above 3 fish/m². Vaccinate if available."
            )
        ))

    @Rule(
        FarmContext(species="tilapia"),
        PhysicalSymptom(symptom="pop_eye"),
        NOT(BehaviorSymptom(symptom="erratic_swimming")),
        salience=10
    )
    def tilapia_streptococcosis_medium_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Streptococcosis — Suspected (Early Stage)",
            cause      = "Bacterial — Streptococcus agalactiae",
            confidence = "Medium",
            urgency    = "Within 24hrs",
            treatment  = (
                "Isolate fish with pop-eye. Monitor tank for spiral swimming. "
                "Reduce feeding. Improve water quality immediately."
            ),
            prevention = (
                "Early isolation is critical — Streptococcosis spreads extremely fast "
                "in high-density ponds."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  DISEASE 4: Ichthyophthirius multifiliis (Ich / White Spot)
    #  Cause   : Ichthyophthirius multifiliis (Parasitic Protozoan)
    #  Trigger : Temperature fluctuation + stressed/new fish
    #  Hallmark: Salt-grain white spots + flashing behavior
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="tilapia"),
        PhysicalSymptom(symptom="white_spots"),
        BehaviorSymptom(symptom="flashing"),
        salience=20
    )
    def tilapia_ich_high_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Ichthyophthirius (White Spot / Ich)",
            cause      = "Parasitic — Ichthyophthirius multifiliis",
            confidence = "High",
            urgency    = "Immediate",
            treatment  = (
                "1. Gradually raise water temperature to 30–32°C — "
                "this accelerates the parasite lifecycle and makes it vulnerable.\n"
                "2. Salt treatment: 3 g/L NaCl for 5–7 days (effective and cheap).\n"
                "3. Formalin bath: 25 mg/L for 4 hours with strong aeration "
                "(use with extreme caution — monitor fish closely).\n"
                "4. Treat for minimum 2 weeks — the encysted stage (on fish) "
                "is drug-resistant; you must kill the free-swimming stage.\n"
                "5. Do NOT introduce new fish during treatment."
            ),
            prevention = (
                "Quarantine all new fish for 2 weeks before introducing to pond. "
                "Ich is most common when temperature drops below 22°C — "
                "common in Sri Lanka's upcountry farms (Nuwara Eliya, Kandy districts). "
                "Stress from handling or transport triggers outbreaks."
            )
        ))

    @Rule(
        FarmContext(species="tilapia"),
        PhysicalSymptom(symptom="white_spots"),
        NOT(BehaviorSymptom(symptom="flashing")),
        salience=10
    )
    def tilapia_ich_medium_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Ichthyophthirius (White Spot) — Suspected",
            cause      = "Parasitic — Ichthyophthirius multifiliis",
            confidence = "Medium",
            urgency    = "Within 24hrs",
            treatment  = (
                "Examine spots under magnification if possible. "
                "Apply salt (2 g/L) as precaution. "
                "Watch for flashing behavior over next 12 hours."
            ),
            prevention = (
                "Check if new fish were recently added — "
                "Ich is almost always introduced via new stock."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  DISEASE 5: Saprolegniasis (Cotton Fungus)
    #  Cause   : Saprolegnia spp. (Fungal)
    #  Trigger : Cold water + physical injury + immunosuppression
    #  Hallmark: Cotton-wool growth on body/fins/eggs
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="tilapia"),
        PhysicalSymptom(symptom="cotton_growth"),
        salience=20
    )
    def tilapia_saprolegnia_high_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Saprolegniasis (Cotton Mould / Water Mould)",
            cause      = "Fungal — Saprolegnia spp.",
            confidence = "High",
            urgency    = "Within 24hrs",
            treatment  = (
                "1. Salt bath: 10–20 g/L NaCl for 20–30 minutes daily.\n"
                "2. Potassium permanganate bath: 1 g/L for 30–60 seconds "
                "(short dip, not pond-wide application).\n"
                "3. Malachite green (0.1 mg/L) if available and legally permitted — "
                "check Sri Lanka DAPH regulations before use.\n"
                "4. Improve water quality — Saprolegnia is almost always "
                "secondary to another stress or injury."
            ),
            prevention = (
                "Saprolegnia is an opportunistic fungus — it never infects healthy fish. "
                "Find and fix the primary stressor (injury, bacterial infection, low temperature). "
                "Common in upcountry Sri Lankan farms during the cool season."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  DISEASE 6: Environmental Oxygen Stress
    #  Cause   : Environmental (low dissolved oxygen)
    #  Trigger : Algae crash, overfeeding, high temperature
    #  Hallmark: Surface gasping + crowding at inlet
    #  Cross-references WaterAlert for DO
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="tilapia"),
        BehaviorSymptom(symptom="surface_gasping"),
        BehaviorSymptom(symptom="near_inlet_crowding"),
        salience=20
    )
    def tilapia_oxygen_stress_behavioral(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Acute Oxygen Depletion Stress",
            cause      = "Environmental — Low Dissolved Oxygen",
            confidence = "High",
            urgency    = "Immediate",
            treatment  = (
                "1. Activate all aerators immediately.\n"
                "2. Perform emergency 30–50% water exchange with well-oxygenated water.\n"
                "3. Stop ALL feeding — decomposing feed consumes oxygen rapidly.\n"
                "4. Remove dead organic matter from pond bottom.\n"
                "5. If nighttime: highest risk — algae switch from O₂ production "
                "to O₂ consumption after dark."
            ),
            prevention = (
                "Install DO sensor with alarm. Avoid overfeeding. "
                "Monitor for algae blooms (green water) which crash overnight. "
                "Always run aerators from midnight to 8 AM during hot season."
            )
        ))

    @Rule(
        FarmContext(species="tilapia"),
        BehaviorSymptom(symptom="surface_gasping"),
        WaterAlert(parameter="dissolved_o2", level="critical"),
        salience=20
    )
    def tilapia_oxygen_stress_confirmed(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Acute Oxygen Depletion — CONFIRMED by sensor",
            cause      = "Environmental — Low Dissolved Oxygen",
            confidence = "High",
            urgency    = "Immediate",
            treatment  = (
                "DO sensor confirms critical oxygen level. "
                "EMERGENCY: Activate all aerators. 50% water exchange now. "
                "Stop feeding. Clear pond surface of any debris blocking gas exchange."
            ),
            prevention = (
                "Calibrate DO sensor weekly. "
                "Set automatic aeration to trigger below 4 mg/L."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  DISEASE 7: Nitrite Poisoning (Brown Blood Disease)
    #  Cause   : Environmental (high nitrite → methemoglobin)
    #  Cross-references WaterAlert for nitrite
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="tilapia"),
        WaterAlert(parameter="nitrite", level="critical"),
        BehaviorSymptom(symptom="lethargy"),
        salience=20
    )
    def tilapia_nitrite_poisoning(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Nitrite Poisoning (Brown Blood Disease)",
            cause      = "Environmental — High Nitrite (NO₂)",
            confidence = "High",
            urgency    = "Immediate",
            treatment  = (
                "1. Add common salt (NaCl) at 60 kg/ha — chloride ions block "
                "nitrite absorption at the gills (most effective intervention).\n"
                "2. Perform 40% water exchange.\n"
                "3. Stop feeding until nitrite normalizes.\n"
                "4. Inspect gills — blood may appear chocolate brown (diagnostic sign).\n"
                "5. Improve biofilter function."
            ),
            prevention = (
                "Nitrite spikes indicate a broken nitrogen cycle. "
                "Seed pond with nitrifying bacteria. "
                "Never overload pond with feed after a break period."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  CATCH-ALL: Unmatched tilapia symptoms
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="tilapia"),
        OR(BehaviorSymptom(), PhysicalSymptom()),
        NOT(DiseaseDiagnosis()),
        salience=1
    )
    def tilapia_unknown(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Undetermined — Insufficient Symptom Match",
            cause      = "Unknown",
            confidence = "Low",
            urgency    = "Monitor",
            treatment  = (
                "Symptoms do not match a known pattern. "
                "Collect water samples and fish tissue samples. "
                "Contact NAQDA Fish Health Laboratory, Colombo: +94 11 2552 801. "
                "Or submit sample to NARA (National Aquatic Resources Agency)."
            ),
            prevention = (
                "Document all observed symptoms with photos for laboratory submission."
            )
        ))
