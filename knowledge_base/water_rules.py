# Covers: pH, Ammonia, Nitrite, Dissolved O2, Temperature, Salinity, Turbidity
# Species: Tilapia (Oreochromis niloticus) & Shrimp (Litopenaeus vannamei)
#
# Salience priority:
#   30 = critical parameter alerts   (fire first — pond may be dying)
#   20 = warning parameter alerts
#   10 = safe/normal confirmations   (fire last)

from experta import KnowledgeEngine, Rule, MATCH, TEST, NOT
from knowledge_base.facts import (
    FarmContext, WaterQuality, WaterAlert
)


class WaterQualityEngine(KnowledgeEngine):

    # ════════════════════════════════════════════════════════
    #  pH RULES — TILAPIA
    #  Safe range: 6.5 – 8.5
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="tilapia"),
        WaterQuality(ph=MATCH.ph),
        TEST(lambda ph: ph < 6.0),
        salience=30
    )
    def tilapia_ph_critical_low(self, ph):
        self.declare(WaterAlert(
            parameter  = "ph",
            level      = "critical",
            actual     = ph,
            safe_range = "6.5 – 8.5",
            correction = (
                "URGENT: pH is lethally low. Apply agricultural lime (CaCO₃) "
                "at 20–25 kg/ha. Stop all feeding immediately. Increase aeration. "
                "Retest after 2 hours. Do not apply more than 25 kg/ha per application."
            )
        ))

    @Rule(
        FarmContext(species="tilapia"),
        WaterQuality(ph=MATCH.ph),
        TEST(lambda ph: 6.0 <= ph < 6.5),
        salience=20
    )
    def tilapia_ph_warning_low(self, ph):
        self.declare(WaterAlert(
            parameter  = "ph",
            level      = "warning",
            actual     = ph,
            safe_range = "6.5 – 8.5",
            correction = (
                "pH is below optimal. Apply dolomite limestone at 10 kg/ha. "
                "Monitor every 6 hours. Avoid fertilizer application until stable."
            )
        ))

    @Rule(
        FarmContext(species="tilapia"),
        WaterQuality(ph=MATCH.ph),
        TEST(lambda ph: ph > 9.5),
        salience=30
    )
    def tilapia_ph_critical_high(self, ph):
        self.declare(WaterAlert(
            parameter  = "ph",
            level      = "critical",
            actual     = ph,
            safe_range = "6.5 – 8.5",
            correction = (
                "URGENT: pH is lethally high — likely algae bloom. "
                "Perform 40% water exchange immediately. Apply alum at 15 kg/ha "
                "to lower pH. Remove excess algae. Increase water flow."
            )
        ))

    @Rule(
        FarmContext(species="tilapia"),
        WaterQuality(ph=MATCH.ph),
        TEST(lambda ph: 8.5 < ph <= 9.5),
        salience=20
    )
    def tilapia_ph_warning_high(self, ph):
        self.declare(WaterAlert(
            parameter  = "ph",
            level      = "warning",
            actual     = ph,
            safe_range = "6.5 – 8.5",
            correction = (
                "pH elevated — possible algal bloom. Reduce fertilizer input. "
                "Perform 20% water exchange. Monitor dissolved O₂ at dawn "
                "(algae blooms crash O₂ overnight)."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  pH RULES — SHRIMP
    #  Safe range: 7.5 – 8.5
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="shrimp"),
        WaterQuality(ph=MATCH.ph),
        TEST(lambda ph: ph < 7.0),
        salience=30
    )
    def shrimp_ph_critical_low(self, ph):
        self.declare(WaterAlert(
            parameter  = "ph",
            level      = "critical",
            actual     = ph,
            safe_range = "7.5 – 8.5",
            correction = (
                "URGENT: pH critically low for shrimp. Apply hydrated lime "
                "Ca(OH)₂ at 10–15 kg/ha. Shrimp will stop moulting below 7.0. "
                "Cease feeding. Activate all aerators immediately."
            )
        ))

    @Rule(
        FarmContext(species="shrimp"),
        WaterQuality(ph=MATCH.ph),
        TEST(lambda ph: 7.0 <= ph < 7.5),
        salience=20
    )
    def shrimp_ph_warning_low(self, ph):
        self.declare(WaterAlert(
            parameter  = "ph",
            level      = "warning",
            actual     = ph,
            safe_range = "7.5 – 8.5",
            correction = (
                "pH below optimal for shrimp. Apply agricultural lime at 10 kg/ha. "
                "Increase buffer capacity. Avoid acid-forming feeds."
            )
        ))

    @Rule(
        FarmContext(species="shrimp"),
        WaterQuality(ph=MATCH.ph),
        TEST(lambda ph: ph > 9.0),
        salience=30
    )
    def shrimp_ph_critical_high(self, ph):
        self.declare(WaterAlert(
            parameter  = "ph",
            level      = "critical",
            actual     = ph,
            safe_range = "7.5 – 8.5",
            correction = (
                "URGENT: pH too high — ammonia toxicity dramatically increases above 9.0. "
                "Perform 30% water exchange. Reduce algae with shade netting. "
                "Stop feeding until pH stabilizes."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  AMMONIA RULES — TILAPIA
    #  Safe: < 0.02 ppm  |  Warning: 0.02–0.1  |  Critical: > 0.1
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="tilapia"),
        WaterQuality(ammonia=MATCH.nh3),
        TEST(lambda nh3: nh3 > 0.1),
        salience=30
    )
    def tilapia_ammonia_critical(self, nh3):
        self.declare(WaterAlert(
            parameter  = "ammonia",
            level      = "critical",
            actual     = nh3,
            safe_range = "< 0.02 mg/L",
            correction = (
                "URGENT: Toxic ammonia level. Perform 50% water exchange immediately. "
                "Stop all feeding for 48 hours (uneaten feed is main ammonia source). "
                "Apply zeolite at 200 kg/ha to bind ammonia. "
                "Check and repair biofilter if present. Increase aeration."
            )
        ))

    @Rule(
        FarmContext(species="tilapia"),
        WaterQuality(ammonia=MATCH.nh3),
        TEST(lambda nh3: 0.02 <= nh3 <= 0.1),
        salience=20
    )
    def tilapia_ammonia_warning(self, nh3):
        self.declare(WaterAlert(
            parameter  = "ammonia",
            level      = "warning",
            actual     = nh3,
            safe_range = "< 0.02 mg/L",
            correction = (
                "Ammonia rising. Reduce feeding rate by 30%. "
                "Increase aeration. Perform 20% water exchange. "
                "Check stocking density — overcrowding is a primary cause."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  AMMONIA RULES — SHRIMP
    #  Safe: < 0.1 mg/L  |  Warning: 0.1–0.5  |  Critical: > 0.5
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="shrimp"),
        WaterQuality(ammonia=MATCH.nh3),
        TEST(lambda nh3: nh3 > 0.5),
        salience=30
    )
    def shrimp_ammonia_critical(self, nh3):
        self.declare(WaterAlert(
            parameter  = "ammonia",
            level      = "critical",
            actual     = nh3,
            safe_range = "< 0.1 mg/L",
            correction = (
                "URGENT: Lethal ammonia level for shrimp. Emergency 40% water exchange. "
                "Apply zeolite 200–300 kg/ha. Stop feeding for 72 hours. "
                "Ammonia toxicity increases sharply when pH > 8.0 — check pH simultaneously. "
                "Contact NAQDA regional office if mortality begins."
            )
        ))

    @Rule(
        FarmContext(species="shrimp"),
        WaterQuality(ammonia=MATCH.nh3),
        TEST(lambda nh3: 0.1 <= nh3 <= 0.5),
        salience=20
    )
    def shrimp_ammonia_warning(self, nh3):
        self.declare(WaterAlert(
            parameter  = "ammonia",
            level      = "warning",
            actual     = nh3,
            safe_range = "< 0.1 mg/L",
            correction = (
                "Ammonia elevated. Reduce feed by 25%. Apply probiotics (Bacillus spp.) "
                "to improve nitrification. Perform 20% water exchange."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  DISSOLVED OXYGEN RULES — BOTH SPECIES
    #  Safe: > 5 mg/L  |  Warning: 3–5  |  Critical: < 3
    # ════════════════════════════════════════════════════════

    @Rule(
        WaterQuality(dissolved_o2=MATCH.do),
        TEST(lambda do: do < 3.0),
        salience=30
    )
    def do_critical(self, do):
        self.declare(WaterAlert(
            parameter  = "dissolved_o2",
            level      = "critical",
            actual     = do,
            safe_range = "> 5.0 mg/L",
            correction = (
                "URGENT: Oxygen depletion — mass mortality imminent within hours. "
                "Activate ALL aerators immediately. Perform emergency 50% water exchange. "
                "Stop feeding. Remove any dead organic matter from pond floor. "
                "If using paddlewheel aerators, run continuously until DO > 5 mg/L. "
                "Critical risk at dawn — algae consume O₂ overnight."
            )
        ))

    @Rule(
        WaterQuality(dissolved_o2=MATCH.do),
        TEST(lambda do: 3.0 <= do < 5.0),
        salience=20
    )
    def do_warning(self, do):
        self.declare(WaterAlert(
            parameter  = "dissolved_o2",
            level      = "warning",
            actual     = do,
            safe_range = "> 5.0 mg/L",
            correction = (
                "Dissolved oxygen below optimal. Increase aeration duration. "
                "Reduce stocking density if persistent. Avoid feeding at dawn "
                "when DO naturally dips. Monitor overnight."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  TEMPERATURE RULES — TILAPIA
    #  Safe: 25–30°C
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="tilapia"),
        WaterQuality(temperature=MATCH.t),
        TEST(lambda t: t > 35.0),
        salience=30
    )
    def tilapia_temp_critical_high(self, t):
        self.declare(WaterAlert(
            parameter  = "temperature",
            level      = "critical",
            actual     = t,
            safe_range = "25 – 30°C",
            correction = (
                "URGENT: Temperature lethally high. Increase water flow from cooler source. "
                "Add shade netting over pond (40% shade cloth). "
                "Perform water exchange with cooler water. Stop feeding."
            )
        ))

    @Rule(
        FarmContext(species="tilapia"),
        WaterQuality(temperature=MATCH.t),
        TEST(lambda t: t < 20.0),
        salience=30
    )
    def tilapia_temp_critical_low(self, t):
        self.declare(WaterAlert(
            parameter  = "temperature",
            level      = "critical",
            actual     = t,
            safe_range = "25 – 30°C",
            correction = (
                "URGENT: Temperature too low — immune suppression and feeding cessation. "
                "Reduce water exchange (incoming water is colder). "
                "In Sri Lanka this typically occurs in upcountry farms during NE monsoon. "
                "Stop feeding — undigested feed worsens water quality."
            )
        ))

    @Rule(
        FarmContext(species="tilapia"),
        WaterQuality(temperature=MATCH.t),
        TEST(lambda t: 30.0 < t <= 35.0),
        salience=20
    )
    def tilapia_temp_warning_high(self, t):
        self.declare(WaterAlert(
            parameter  = "temperature",
            level      = "warning",
            actual     = t,
            safe_range = "25 – 30°C",
            correction = (
                "Temperature elevated. Monitor DO closely (warm water holds less oxygen). "
                "Consider shade netting. Feed in cooler morning hours only."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  TEMPERATURE RULES — SHRIMP
    #  Safe: 23–30°C
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="shrimp"),
        WaterQuality(temperature=MATCH.t),
        TEST(lambda t: t > 33.0),
        salience=30
    )
    def shrimp_temp_critical_high(self, t):
        self.declare(WaterAlert(
            parameter  = "temperature",
            level      = "critical",
            actual     = t,
            safe_range = "23 – 30°C",
            correction = (
                "URGENT: Temperature critical for shrimp. High temperature accelerates "
                "Vibrio bacteria growth exponentially. Increase water exchange. "
                "Add shade netting. Reduce feeding to 50%."
            )
        ))

    @Rule(
        FarmContext(species="shrimp"),
        WaterQuality(temperature=MATCH.t),
        TEST(lambda t: t < 20.0),
        salience=30
    )
    def shrimp_temp_critical_low(self, t):
        self.declare(WaterAlert(
            parameter  = "temperature",
            level      = "critical",
            actual     = t,
            safe_range = "23 – 30°C",
            correction = (
                "URGENT: Temperature too low. Shrimp immune system severely compromised. "
                "Cease feeding. Reduce water exchange. "
                "EMS/AHPND risk increases at low temperatures."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  SALINITY RULES — SHRIMP ONLY
    #  Safe: 10–25 ppt
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="shrimp"),
        WaterQuality(salinity=MATCH.sal),
        TEST(lambda sal: sal < 5.0),
        salience=30
    )
    def shrimp_salinity_critical_low(self, sal):
        self.declare(WaterAlert(
            parameter  = "salinity",
            level      = "critical",
            actual     = sal,
            safe_range = "10 – 25 ppt",
            correction = (
                "URGENT: Salinity critically low — osmotic stress. "
                "Gradually add sea water or salt to raise salinity. "
                "Do NOT change salinity more than 2–3 ppt per day to avoid osmotic shock. "
                "This is common in Sri Lankan coastal farms after heavy rainfall."
            )
        ))

    @Rule(
        FarmContext(species="shrimp"),
        WaterQuality(salinity=MATCH.sal),
        TEST(lambda sal: 5.0 <= sal < 10.0),
        salience=20
    )
    def shrimp_salinity_warning_low(self, sal):
        self.declare(WaterAlert(
            parameter  = "salinity",
            level      = "warning",
            actual     = sal,
            safe_range = "10 – 25 ppt",
            correction = (
                "Salinity below optimal. Gradually increase with seawater addition. "
                "Monitor moulting — shrimp are vulnerable to disease post-moult "
                "when salinity is unstable."
            )
        ))

    @Rule(
        FarmContext(species="shrimp"),
        WaterQuality(salinity=MATCH.sal),
        TEST(lambda sal: sal > 35.0),
        salience=30
    )
    def shrimp_salinity_critical_high(self, sal):
        self.declare(WaterAlert(
            parameter  = "salinity",
            level      = "critical",
            actual     = sal,
            safe_range = "10 – 25 ppt",
            correction = (
                "URGENT: Salinity too high — severe osmotic stress. "
                "Dilute with freshwater gradually (max 3 ppt/day change). "
                "Increase aeration — high salinity reduces oxygen solubility."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  NITRITE RULES — BOTH SPECIES
    #  Safe: < 0.1 mg/L  |  Warning: 0.1–0.5  |  Critical: > 0.5
    # ════════════════════════════════════════════════════════

    @Rule(
        WaterQuality(nitrite=MATCH.no2),
        TEST(lambda no2: no2 > 0.5),
        salience=30
    )
    def nitrite_critical(self, no2):
        self.declare(WaterAlert(
            parameter  = "nitrite",
            level      = "critical",
            actual     = no2,
            safe_range = "< 0.1 mg/L",
            correction = (
                "URGENT: Nitrite at toxic levels — brown blood disease risk. "
                "Nitrite blocks oxygen transport in blood. Perform 40% water exchange. "
                "Add common salt (NaCl) at 60 kg/ha — chloride ions compete with nitrite "
                "at gill uptake sites. Check biofilter bacteria colonies."
            )
        ))

    @Rule(
        WaterQuality(nitrite=MATCH.no2),
        TEST(lambda no2: 0.1 <= no2 <= 0.5),
        salience=20
    )
    def nitrite_warning(self, no2):
        self.declare(WaterAlert(
            parameter  = "nitrite",
            level      = "warning",
            actual     = no2,
            safe_range = "< 0.1 mg/L",
            correction = (
                "Nitrite elevated. Reduce feeding. Perform 25% water exchange. "
                "Check that biofilter is running correctly. "
                "Add beneficial bacteria (nitrifying bacteria product) if available."
            )
        ))

    # ════════════════════════════════════════════════════════
    #  TURBIDITY RULES — SHRIMP ONLY
    #  Safe: 30–40 NTU  |  Warning: <20 or >60  |  Critical: <10 or >100
    # ════════════════════════════════════════════════════════

    @Rule(
        FarmContext(species="shrimp"),
        WaterQuality(turbidity=MATCH.ntu),
        TEST(lambda ntu: ntu > 100),
        salience=30
    )
    def shrimp_turbidity_critical_high(self, ntu):
        self.declare(WaterAlert(
            parameter  = "turbidity",
            level      = "critical",
            actual     = ntu,
            safe_range = "30 – 40 NTU",
            correction = (
                "URGENT: Extreme turbidity — likely mud/clay suspension or algae bloom. "
                "Apply alum (aluminum sulfate) at 10–15 kg/ha to flocculate particles. "
                "Reduce water inlet. Check for pond bank erosion."
            )
        ))

    @Rule(
        FarmContext(species="shrimp"),
        WaterQuality(turbidity=MATCH.ntu),
        TEST(lambda ntu: ntu < 10),
        salience=20
    )
    def shrimp_turbidity_critical_low(self, ntu):
        self.declare(WaterAlert(
            parameter  = "turbidity",
            level      = "warning",
            actual     = ntu,
            safe_range = "30 – 40 NTU",
            correction = (
                "Water too clear — shrimp are stressed without plankton cover. "
                "Apply organic fertilizer to encourage phytoplankton growth. "
                "Shrimp become cannibalistic in overly clear water."
            )
        ))