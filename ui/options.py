"""Shared UI option definitions for desktop and web interfaces."""

BEHAVIOR_SYMPTOMS = [
    ("surface_gasping", "Surface gasping / gulping air"),
    ("erratic_swimming", "Erratic / spiral swimming"),
    ("lethargy", "Lethargy / sitting at bottom"),
    ("flashing", "Flashing / rubbing on surfaces"),
    ("reduced_feeding", "Reduced or stopped feeding"),
    ("mass_mortality", "Mass mortality (sudden deaths)"),
    ("whirling", "Whirling / spinning (shrimp)"),
    ("near_inlet_crowding", "Crowding near water inlet"),
]

PHYSICAL_SYMPTOMS = [
    ("hemorrhagic_ulcer", "body", "Hemorrhagic ulcers / bloody sores"),
    ("white_spots", "body", "White spots (salt-grain size) on body"),
    ("shell_white_spots", "shell", "White spots visible under shell (shrimp)"),
    ("white_patches", "body", "White / grey patches on body"),
    ("cotton_growth", "body", "Cotton-wool / fluffy growth"),
    ("fin_erosion", "fin", "Fin erosion / fraying"),
    ("pop_eye", "eye", "Pop-eye / bulging eye"),
    ("body_darkening", "body", "Body darkening / discoloration"),
    ("red_discoloration", "body", "Red discoloration on body or legs"),
    ("black_gills", "gill", "Black / dark gills"),
    ("white_muscle", "body", "White muscle (shrimp)"),
    ("soft_shell", "shell", "Soft shell / not hardening (shrimp)"),
    ("white_hepatopancreas", "body", "White/pale digestive gland (shrimp)"),
    ("empty_stomach", "body", "Empty / transparent stomach (shrimp)"),
]

WATER_FIELDS = [
    ("ph", "pH", "6.5-8.5 (Tilapia) | 7.5-8.5 (Shrimp)"),
    ("ammonia", "Ammonia - NH3 (mg/L)", "< 0.02 (Tilapia) | < 0.1 (Shrimp)"),
    ("nitrite", "Nitrite - NO2 (mg/L)", "< 0.1"),
    ("dissolved_o2", "Dissolved O2 (mg/L)", "> 5.0"),
    ("temperature", "Temperature (C)", "25-30 (Tilapia) | 23-30 (Shrimp)"),
    ("salinity", "Salinity (ppt)", "10-25 (Shrimp only)"),
    ("turbidity", "Turbidity (NTU)", "30-40 (Shrimp only)"),
]
