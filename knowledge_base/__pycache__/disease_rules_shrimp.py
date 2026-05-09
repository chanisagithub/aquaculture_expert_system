# knowledge_base/disease_rules_shrimp.py
# Disease Diagnosis Rules — Whiteleg Shrimp (Litopenaeus vannamei)
#
# Diseases covered:
#   1. White Spot Syndrome Virus (WSSV)
#   2. Early Mortality Syndrome (EMS / AHPND)
#   3. Vibriosis
#   4. Black Gill Disease
#   5. Loose Shell Syndrome (LSS)
#   6. Enterocytozoon hepatopenaei (EHP) / Running Mortality Syndrome
#
# Cross-referencing:
#   Several rules also match WaterAlert facts — poor water quality
#   dramatically increases disease susceptibility in shrimp.
#
# Salience:
#   30 = mass mortality / viral — most urgent possible
#   20 = high confidence bacterial/parasitic
#   10 = medium confidence
#    5 = low / single indicator
#    1 = catch-all

from experta import KnowledgeEngine, Rule, MATCH, OR, NOT, salience
from knowledge_base.facts import (
    FarmContext, BehaviorSymptom, PhysicalSymptom,
    WaterAlert, DiseaseDiagnosis
)


class ShrimpDiseaseEngine(KnowledgeEngine):

    # ════════════════════════════════════════════════════════
    #  DISEASE 1: White Spot Syndrome Virus (WSSV)
    #  Cause   : White Spot Syndrome Virus (Viral — no cure)
    #  Trigger : Infected broodstock / water / wild carriers
    #  Hallmark: White spots under shell + sudden mass mortality
    #  NOTE    : Most catastrophic shrimp disease globally.
    #            Destroyed Sri Lanka's shrimp industry in early 2000s.
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="shrimp"),
        PhysicalSymptom(symptom="shell_white_spots"),
        BehaviorSymptom(symptom="mass_mortality"),
        salience(30)
    )
    def shrimp_wssv_high_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "White Spot Syndrome Virus (WSSV)",
            cause      = "Viral — White Spot Syndrome Virus",
            confidence = "High",
            urgency    = "Immediate",
            treatment  = (
                "WARNING: There is NO cure for WSSV.\n"
                "1. IMMEDIATELY cease all water exchange to prevent "
                "virus escaping to adjacent water bodies.\n"
                "2. Do NOT harvest and sell — notify NAQDA immediately: "
                "+94 31 222 7780 (Chilaw Regional Office).\n"
                "3. Emergency harvest only if >50% mortality has not yet occurred "
                "— sell for processing, not live market.\n"
                "4. After depopulation: drain pond completely. "
                "Apply calcium hypochlorite (chlorine) at 30 ppm. "
                "Sun-dry pond bed for minimum 3 weeks.\n"
                "5. Do not restock for at least 60 days.\n"
                "6. Destroy all nets, equipment in contact with infected water "
                "or disinfect with 200 ppm chlorine for 24 hours."
            ),
            prevention = (
                "Use only SPF (Specific Pathogen Free) certified post-larvae "
                "from accredited hatcheries (NAQDA certified). "
                "Screen all water intake with 200-micron filters. "
                "Control wild crustaceans entering pond — crabs and crayfish "
                "are WSSV carriers. Install bird netting — herons are vectors. "
                "WSSV devastated Sri Lanka's Puttalam and Chilaw farms in 2003–2006."
            )
        ))

    @Rule(
        FarmContext(species="shrimp"),
        PhysicalSymptom(symptom="shell_white_spots"),
        NOT(BehaviorSymptom(symptom="mass_mortality")),
        salience(20)
    )
    def shrimp_wssv_medium_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "White Spot Syndrome Virus (WSSV) — Suspected",
            cause      = "Viral — White Spot Syndrome Virus",
            confidence = "Medium",
            urgency    = "Immediate",
            treatment  = (
                "White spots without mass mortality may be early WSSV or calcium "
                "deficiency (loose shell). Do NOT wait to confirm.\n"
                "1. Stop water exchange immediately.\n"
                "2. Collect 10 shrimp samples and send to NARA Fish Disease "
                "Laboratory for PCR test — results within 24–48 hours.\n"
                "3. Prepare for emergency harvest if PCR confirms WSSV.\n"
                "4. Notify NAQDA regional office."
            ),
            prevention = (
                "White spots without mortality — also rule out calcium deficiency. "
                "Check alkalinity and calcium levels. "
                "WSSV confirmation requires PCR — do not self-diagnose and delay action."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  DISEASE 2: Early Mortality Syndrome (EMS / AHPND)
    #  Cause   : Vibrio parahaemolyticus — produces hepatotoxin
    #  Trigger : Poor water + overstocking + first 30 days post-stocking
    #  Hallmark: Empty stomach + white hepatopancreas + mass death < day 30
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="shrimp"),
        PhysicalSymptom(symptom="empty_stomach"),
        PhysicalSymptom(symptom="white_hepatopancreas"),
        BehaviorSymptom(symptom="mass_mortality"),
        salience(30)
    )
    def shrimp_ems_high_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Early Mortality Syndrome (EMS / AHPND)",
            cause      = "Bacterial — Vibrio parahaemolyticus (AHPND strain)",
            confidence = "High",
            urgency    = "Immediate",
            treatment  = (
                "WARNING: EMS kills 100% of shrimp within 3–5 days of onset.\n"
                "1. Emergency harvest immediately — do not wait.\n"
                "2. If early-stage (< 20% mortality): apply probiotics "
                "(Bacillus subtilis, B. licheniformis) and reduce feeding to zero.\n"
                "3. Perform 50% water exchange.\n"
                "4. If antibiotic treatment is chosen (vet prescription required): "
                "Oxytetracycline in feed — but efficacy is limited once toxin is produced.\n"
                "5. Disinfect pond with chlorine (30 ppm) after depopulation.\n"
                "6. Report to NAQDA — EMS is a notifiable disease in Sri Lanka."
            ),
            prevention = (
                "EMS strikes in the first 30 days — highest risk period. "
                "Use only certified SPF post-larvae. "
                "Add probiotics to feed from day 1 of stocking. "
                "Maintain zero discharge policy during first month. "
                "Screen source water for Vibrio before stocking. "
                "Avoid stocking during temperature extremes (< 23°C or > 31°C)."
            )
        ))

    @Rule(
        FarmContext(species="shrimp"),
        PhysicalSymptom(symptom="empty_stomach"),
        PhysicalSymptom(symptom="white_hepatopancreas"),
        NOT(BehaviorSymptom(symptom="mass_mortality")),
        salience(20)
    )
    def shrimp_ems_medium_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Early Mortality Syndrome (EMS) — Suspected (Early Stage)",
            cause      = "Bacterial — Vibrio parahaemolyticus",
            confidence = "Medium",
            urgency    = "Immediate",
            treatment  = (
                "Early EMS detected before mass mortality — act now.\n"
                "1. Stop feeding completely.\n"
                "2. Apply probiotics to water column immediately.\n"
                "3. Perform 30% water exchange with pathogen-screened water.\n"
                "4. Collect 5 shrimp for NARA laboratory PCR confirmation.\n"
                "5. Prepare for emergency harvest if mortality begins within 24h."
            ),
            prevention = (
                "Hepatopancreas discoloration is the earliest visible sign of EMS. "
                "Daily observation of a sample of shrimp during first 30 days is essential."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  DISEASE 3: Vibriosis
    #  Cause   : Vibrio spp. (harveyi, alginolyticus, vulnificus)
    #  Trigger : High temperature + high organic load + poor DO
    #  Hallmark: Luminescence at night + red discoloration + lethargy
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="shrimp"),
        PhysicalSymptom(symptom="red_discoloration"),
        BehaviorSymptom(symptom="lethargy"),
        salience(20)
    )
    def shrimp_vibriosis_high_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Vibriosis",
            cause      = "Bacterial — Vibrio spp. (harveyi / alginolyticus)",
            confidence = "High",
            urgency    = "Immediate",
            treatment  = (
                "1. Reduce feeding to 50% — organic matter feeds Vibrio.\n"
                "2. Apply probiotics (Bacillus spp.) at 5 ppm across pond.\n"
                "3. Perform 30% water exchange.\n"
                "4. Apply disinfectant: Povidone-iodine at 1 ppm or "
                "BKC (benzalkonium chloride) at 0.5 ppm.\n"
                "5. For severe cases: Oxytetracycline or Florfenicol "
                "(vet prescription required).\n"
                "6. Check water temperature — Vibrio thrives above 30°C. "
                "Install shade netting if temperature is elevated."
            ),
            prevention = (
                "Vibrio is naturally present in all marine/brackish water — "
                "the goal is population control, not elimination. "
                "Maintain DO > 5 mg/L. Avoid overfeeding. "
                "Weekly probiotic application is the most effective prevention. "
                "Vibriosis risk peaks during Sri Lanka's southwest monsoon "
                "(May–September) when temperatures and organic load both peak."
            )
        ))

    @Rule(
        FarmContext(species="shrimp"),
        PhysicalSymptom(symptom="red_discoloration"),
        WaterAlert(parameter="temperature", level="critical"),
        salience(20)
    )
    def shrimp_vibriosis_heat_linked(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Vibriosis — Temperature-Triggered",
            cause      = "Bacterial — Vibrio spp. (heat-accelerated bloom)",
            confidence = "High",
            urgency    = "Immediate",
            treatment  = (
                "Critical temperature is accelerating Vibrio growth exponentially.\n"
                "1. FIRST: Address water temperature (see Water Alerts above).\n"
                "2. Apply Bacillus probiotics 5 ppm immediately.\n"
                "3. Stop feeding until temperature normalizes.\n"
                "4. Increase aeration — high temperature also reduces dissolved O₂."
            ),
            prevention = (
                "Install a thermometer with logging. "
                "Vibrio doubling time drops from hours to minutes above 32°C."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  DISEASE 4: Black Gill Disease
    #  Cause   : Bacterial / Parasitic / Environmental
    #  Trigger : High ammonia + poor aeration + organic sediment
    #  Hallmark: Dark/black gill coloration + reduced feeding + erratic swim
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="shrimp"),
        PhysicalSymptom(symptom="black_gills", location="gill"),
        BehaviorSymptom(symptom="reduced_feeding"),
        salience(20)
    )
    def shrimp_black_gill_high_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Black Gill Disease",
            cause      = "Bacterial / Parasitic / Environmental (multi-etiology)",
            confidence = "High",
            urgency    = "Within 24hrs",
            treatment  = (
                "1. Test and address ammonia and nitrite levels first "
                "(black gills are often caused by chronic ammonia exposure).\n"
                "2. Siphon pond bottom to remove black organic sediment.\n"
                "3. Apply EDTA at 2–5 ppm to chelate heavy metals if pond is old.\n"
                "4. Increase aeration — improve water circulation near bottom.\n"
                "5. Apply potassium permanganate (KMnO₄) at 1–2 ppm "
                "if parasites are confirmed under microscope.\n"
                "6. Reduce feeding and check FCR."
            ),
            prevention = (
                "Black gill is common in late-culture-cycle ponds (60+ days) "
                "when sediment accumulates. "
                "Siphon pond bottom every 2 weeks. "
                "Maintain water exchange to flush hydrogen sulfide from sediment."
            )
        ))

    @Rule(
        FarmContext(species="shrimp"),
        PhysicalSymptom(symptom="black_gills", location="gill"),
        WaterAlert(parameter="ammonia", level="critical"),
        salience(20)
    )
    def shrimp_black_gill_ammonia_linked(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Black Gill Disease — Ammonia-Induced",
            cause      = "Environmental — Chronic Ammonia Exposure",
            confidence = "High",
            urgency    = "Immediate",
            treatment  = (
                "Ammonia is confirmed as the primary driver of gill damage.\n"
                "1. Emergency water exchange 40%.\n"
                "2. Apply zeolite 200 kg/ha to bind ammonia.\n"
                "3. Stop feeding for 48 hours.\n"
                "4. The gill discoloration will not reverse immediately — "
                "focus on stopping further damage."
            ),
            prevention = (
                "Chronic ammonia exposure over days causes irreversible gill damage. "
                "Test ammonia daily in high-density ponds."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  DISEASE 5: Loose Shell Syndrome (LSS)
    #  Cause   : Nutritional / Bacterial / Environmental
    #  Trigger : Mineral deficiency + Vibrio + rapid growth phase
    #  Hallmark: Shell not hardening post-moult + shell separated from body
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="shrimp"),
        PhysicalSymptom(symptom="soft_shell"),
        BehaviorSymptom(symptom="reduced_feeding"),
        salience(20)
    )
    def shrimp_lss_high_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Loose Shell Syndrome (LSS)",
            cause      = "Nutritional / Bacterial — Vibrio spp.",
            confidence = "High",
            urgency    = "Within 24hrs",
            treatment  = (
                "1. Check and correct salinity — low salinity reduces mineral "
                "availability for shell hardening.\n"
                "2. Add calcium (Ca²⁺) and magnesium supplements to pond.\n"
                "3. Apply probiotics (Bacillus) to suppress Vibrio colonization "
                "of post-moult shrimp.\n"
                "4. Reduce feeding — post-moult shrimp cannot eat hard pellets.\n"
                "5. Avoid pond disturbance during suspected mass moulting periods "
                "(typically every 7–10 days at 30-day-old culture)."
            ),
            prevention = (
                "Maintain alkalinity at 120–150 mg/L CaCO₃. "
                "Ensure feed contains adequate phosphorus and calcium. "
                "Soft-shelled shrimp are extremely vulnerable to cannibalism — "
                "LSS can trigger cascade mortality if not controlled."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  DISEASE 6: EHP / Running Mortality Syndrome
    #  Cause   : Enterocytozoon hepatopenaei (Microsporidian parasite)
    #  Trigger : Contaminated feed / water / broodstock
    #  Hallmark: Slow whirling + white muscle + stunted growth
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="shrimp"),
        BehaviorSymptom(symptom="whirling"),
        PhysicalSymptom(symptom="white_muscle"),
        salience(20)
    )
    def shrimp_ehp_high_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "EHP / Running Mortality Syndrome (RMS)",
            cause      = "Parasitic — Enterocytozoon hepatopenaei (Microsporidian)",
            confidence = "High",
            urgency    = "Within 24hrs",
            treatment  = (
                "1. No fully effective commercial treatment exists for EHP.\n"
                "2. Fumagillin has been used experimentally but is restricted in "
                "many countries — check Sri Lanka DAPH status before use.\n"
                "3. Reduce stocking density to slow transmission.\n"
                "4. Remove and destroy all dead/moribund shrimp immediately.\n"
                "5. Disinfect pond bottom with chlorine after harvest.\n"
                "6. Send samples to NARA for PCR-based EHP confirmation."
            ),
            prevention = (
                "EHP is transmitted through infected feces and pond sediment. "
                "Use only PCR-tested SPF post-larvae. "
                "Never reuse pond water from a previous infected crop. "
                "EHP is increasingly reported in Sri Lanka's northwestern province farms. "
                "Full pond drying between crops is the most effective break in the cycle."
            )
        ))

    @Rule(
        FarmContext(species="shrimp"),
        BehaviorSymptom(symptom="whirling"),
        NOT(PhysicalSymptom(symptom="white_muscle")),
        salience(10)
    )
    def shrimp_ehp_medium_confidence(self):
        self.declare(DiseaseDiagnosis(
            disease    = "EHP / Running Mortality Syndrome — Suspected",
            cause      = "Parasitic — Enterocytozoon hepatopenaei",
            confidence = "Medium",
            urgency    = "Within 24hrs",
            treatment  = (
                "Whirling without white muscle — could also be neurological "
                "from pesticide contamination or Vibrio neurotoxin.\n"
                "1. Collect shrimp samples for NARA PCR test.\n"
                "2. Check nearby agricultural fields for pesticide runoff "
                "(common in Sri Lanka's North Western Province farming belt).\n"
                "3. Reduce feeding. Increase aeration."
            ),
            prevention = (
                "Monitor growth rate weekly — stunted growth (FCR > 2.0) "
                "is the earliest economic sign of EHP before visible symptoms appear."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  CATCH-ALL: Unmatched shrimp symptoms
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="shrimp"),
        OR(BehaviorSymptom(), PhysicalSymptom()),
        NOT(DiseaseDiagnosis()),
        salience(1)
    )
    def shrimp_unknown(self):
        self.declare(DiseaseDiagnosis(
            disease    = "Undetermined — Insufficient Symptom Match",
            cause      = "Unknown",
            confidence = "Low",
            urgency    = "Monitor",
            treatment  = (
                "Symptoms do not match a known pattern in the knowledge base.\n"
                "Contact: NAQDA National Aquaculture Development Authority\n"
                "  Hotline : +94 31 222 7780\n"
                "  NARA Fish Disease Lab (Crow Island, Colombo 15)\n"
                "  Email   : info@nara.ac.lk\n"
                "Collect 10 live symptomatic shrimp in aerated water for lab submission."
            ),
            prevention = (
                "Photograph all visible symptoms. Record water parameters at time "
                "of observation. This data is critical for lab diagnosis."
            )
        ))