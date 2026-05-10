# ui/app.py
# Tkinter UI — Aquaculture Expert System
# Layout: 4-tab notebook → [Farm Setup] [Water Quality] [Symptoms] [Results]

import tkinter as tk
from tkinter import ttk, scrolledtext, font
from engine.master_engine import run_full_diagnosis

# ── Color palette ─────────────────────────────────────────────────────────────
COLORS = {
    "bg"          : "#f0f4f8",
    "panel"       : "#ffffff",
    "accent"      : "#1a6b3c",       # deep green
    "accent_light": "#e8f5e9",
    "critical"    : "#c62828",
    "critical_bg" : "#ffebee",
    "warning"     : "#e65100",
    "warning_bg"  : "#fff3e0",
    "stable"      : "#1a6b3c",
    "stable_bg"   : "#e8f5e9",
    "text"        : "#212121",
    "subtext"     : "#546e7a",
    "border"      : "#cfd8dc",
    "button"      : "#1a6b3c",
    "button_text" : "#111111",
    "tab_active"  : "#1a6b3c",
}

# ── Symptom definitions ───────────────────────────────────────────────────────
BEHAVIOR_SYMPTOMS = [
    ("surface_gasping",    "Surface gasping / gulping air"),
    ("erratic_swimming",   "Erratic / spiral swimming"),
    ("lethargy",           "Lethargy / sitting at bottom"),
    ("flashing",           "Flashing / rubbing on surfaces"),
    ("reduced_feeding",    "Reduced or stopped feeding"),
    ("mass_mortality",     "Mass mortality (sudden deaths)"),
    ("whirling",           "Whirling / spinning (shrimp)"),
    ("near_inlet_crowding","Crowding near water inlet"),
]

PHYSICAL_SYMPTOMS = [
    ("hemorrhagic_ulcer",    "body",  "Hemorrhagic ulcers / bloody sores"),
    ("white_spots",          "body",  "White spots (salt-grain size) on body"),
    ("shell_white_spots",    "shell", "White spots visible under shell (shrimp)"),
    ("white_patches",        "body",  "White / grey patches on body"),
    ("cotton_growth",        "body",  "Cotton-wool / fluffy growth"),
    ("fin_erosion",          "fin",   "Fin erosion / fraying"),
    ("pop_eye",              "eye",   "Pop-eye / bulging eye"),
    ("body_darkening",       "body",  "Body darkening / discoloration"),
    ("red_discoloration",    "body",  "Red discoloration on body or legs"),
    ("black_gills",          "gill",  "Black / dark gills"),
    ("white_muscle",         "body",  "White muscle (shrimp)"),
    ("soft_shell",           "shell", "Soft shell / not hardening (shrimp)"),
    ("white_hepatopancreas", "body",  "White/pale digestive gland (shrimp)"),
    ("empty_stomach",        "body",  "Empty / transparent stomach (shrimp)"),
]


class AquaExpertApp:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Aquaculture Disease & Water Quality Expert System")
        self.root.geometry("860x680")
        self.root.configure(bg=COLORS["bg"])
        self.root.resizable(True, True)

        self._init_vars()
        self._build_header()
        self._build_notebook()
        self._build_footer()

    # ── Variable initialization ───────────────────────────────────────────────
    def _init_vars(self):
        self.species_var       = tk.StringVar(value="shrimp")
        self.pond_age_var      = tk.StringVar(value="")
        self.stocking_var      = tk.StringVar(value="medium")

        # Water quality inputs
        self.water_vars = {
            "ph"          : tk.StringVar(),
            "ammonia"     : tk.StringVar(),
            "nitrite"     : tk.StringVar(),
            "dissolved_o2": tk.StringVar(),
            "temperature" : tk.StringVar(),
            "salinity"    : tk.StringVar(),
            "turbidity"   : tk.StringVar(),
        }

        # Symptom checkboxes
        self.behavior_vars = {k: tk.BooleanVar() for k, _ in BEHAVIOR_SYMPTOMS}
        self.physical_vars = {k: tk.BooleanVar() for k, _, _ in PHYSICAL_SYMPTOMS}

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self.root, bg=COLORS["accent"], pady=12)
        hdr.pack(fill="x")

        tk.Label(
            hdr, text="🐟  Aquaculture Expert System",
            font=("Helvetica", 17, "bold"),
            bg=COLORS["accent"], fg="white"
        ).pack()

        tk.Label(
            hdr,
            text="Fish Disease Diagnosis & Water Quality Analysis  |  "
                 "Artificial Cognitive Systems — University of Moratuwa",
            font=("Helvetica", 8),
            bg=COLORS["accent"], fg="#a5d6a7"
        ).pack()

    # ── Notebook (tabs) ───────────────────────────────────────────────────────
    def _build_notebook(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",       background=COLORS["bg"], borderwidth=0)
        style.configure("TNotebook.Tab",   padding=[16, 6], font=("Helvetica", 10))
        style.map("TNotebook.Tab",
                  background=[("selected", COLORS["accent"])],
                  foreground=[("selected", "white")])

        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True, padx=16, pady=(10, 0))

        self._build_tab_farm()
        self._build_tab_water()
        self._build_tab_symptoms()
        self._build_tab_results()

    # ── Tab 1: Farm Setup ─────────────────────────────────────────────────────
    def _build_tab_farm(self):
        tab = self._make_tab("🏡  Farm Setup")

        # Species selector
        sec = self._section(tab, "Species")
        for val, label in [("tilapia", "🐟  Tilapia (Oreochromis niloticus)"),
                           ("shrimp",  "🦐  Whiteleg Shrimp (Litopenaeus vannamei)")]:
            ttk.Radiobutton(
                sec, text=label, variable=self.species_var,
                value=val, style="TRadiobutton"
            ).pack(anchor="w", pady=3, padx=10)

        # Pond details
        sec2 = self._section(tab, "Pond Details  (optional)")
        row = tk.Frame(sec2, bg=COLORS["panel"])
        row.pack(fill="x", padx=10, pady=4)

        tk.Label(row, text="Days since stocking:", bg=COLORS["panel"],
                 fg=COLORS["text"], width=22, anchor="w").grid(row=0, column=0, sticky="w")
        ttk.Entry(row, textvariable=self.pond_age_var, width=10).grid(row=0, column=1, padx=6)

        tk.Label(row, text="Stocking density:", bg=COLORS["panel"],
                 fg=COLORS["text"], width=22, anchor="w").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Combobox(
            row, textvariable=self.stocking_var,
            values=["low", "medium", "high"], width=10, state="readonly"
        ).grid(row=1, column=1, padx=6)

        # Tip
        tk.Label(
            tab,
            text="💡  Tip: Days since stocking is especially important for shrimp — "
                 "EMS typically strikes within the first 30 days.",
            font=("Helvetica", 9, "italic"), fg=COLORS["subtext"],
            bg=COLORS["bg"], wraplength=700, justify="left"
        ).pack(anchor="w", padx=10, pady=(12, 0))

    # ── Tab 2: Water Quality ──────────────────────────────────────────────────
    def _build_tab_water(self):
        tab = self._make_tab("💧  Water Quality")

        sec = self._section(tab, "Enter Water Parameter Readings  (leave blank if not measured)")

        fields = [
            ("ph",           "pH",                    "6.5–8.5  (Tilapia)   |   7.5–8.5  (Shrimp)"),
            ("ammonia",      "Ammonia — NH₃ (mg/L)",  "< 0.02  (Tilapia)    |   < 0.1   (Shrimp)"),
            ("nitrite",      "Nitrite — NO₂ (mg/L)",  "< 0.1"),
            ("dissolved_o2", "Dissolved O₂ (mg/L)",   "> 5.0"),
            ("temperature",  "Temperature (°C)",       "25–30  (Tilapia)     |   23–30   (Shrimp)"),
            ("salinity",     "Salinity (ppt) 🦐",      "10–25  (Shrimp only)"),
            ("turbidity",    "Turbidity (NTU) 🦐",     "30–40  (Shrimp only)"),
        ]

        grid = tk.Frame(sec, bg=COLORS["panel"])
        grid.pack(fill="x", padx=10, pady=6)

        # Column headers
        for col, text in enumerate(["Parameter", "Your Reading", "Safe Range"]):
            tk.Label(
                grid, text=text,
                font=("Helvetica", 9, "bold"),
                bg=COLORS["panel"], fg=COLORS["accent"], width=28, anchor="w"
            ).grid(row=0, column=col, padx=4, pady=(0, 6))

        for i, (key, label, safe) in enumerate(fields, start=1):
            tk.Label(
                grid, text=label,
                bg=COLORS["panel"], fg=COLORS["text"], anchor="w", width=28
            ).grid(row=i, column=0, padx=4, pady=3, sticky="w")

            ttk.Entry(
                grid, textvariable=self.water_vars[key], width=12
            ).grid(row=i, column=1, padx=4, pady=3)

            tk.Label(
                grid, text=safe,
                bg=COLORS["panel"], fg=COLORS["subtext"],
                font=("Helvetica", 8), anchor="w"
            ).grid(row=i, column=2, padx=4, pady=3, sticky="w")

    # ── Tab 3: Symptoms ───────────────────────────────────────────────────────
    def _build_tab_symptoms(self):
        tab = self._make_tab("🔬  Symptoms")

        # Make tab scrollable
        canvas = tk.Canvas(tab, bg=COLORS["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COLORS["bg"])

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Behavior symptoms
        b_sec = self._section(scroll_frame, "Behavioral Symptoms")
        for key, label in BEHAVIOR_SYMPTOMS:
            tk.Checkbutton(
                b_sec, text=label,
                variable=self.behavior_vars[key],
                bg=COLORS["panel"], fg=COLORS["text"],
                activebackground=COLORS["panel"],
                font=("Helvetica", 10), anchor="w"
            ).pack(anchor="w", padx=14, pady=2)

        # Physical symptoms
        p_sec = self._section(scroll_frame, "Physical / Visual Symptoms")
        for key, loc, label in PHYSICAL_SYMPTOMS:
            tk.Checkbutton(
                p_sec, text=label,
                variable=self.physical_vars[key],
                bg=COLORS["panel"], fg=COLORS["text"],
                activebackground=COLORS["panel"],
                font=("Helvetica", 10), anchor="w"
            ).pack(anchor="w", padx=14, pady=2)

    # ── Tab 4: Results ────────────────────────────────────────────────────────
    def _build_tab_results(self):
        tab = self._make_tab("📋  Results")

        # Status banner (updated after diagnosis)
        self.status_frame = tk.Frame(tab, bg=COLORS["bg"], pady=6)
        self.status_frame.pack(fill="x", padx=10)

        self.status_label = tk.Label(
            self.status_frame,
            text="Run a diagnosis to see results.",
            font=("Helvetica", 12, "bold"),
            bg=COLORS["bg"], fg=COLORS["subtext"]
        )
        self.status_label.pack()

        self.summary_label = tk.Label(
            self.status_frame, text="",
            font=("Helvetica", 9), fg=COLORS["subtext"],
            bg=COLORS["bg"], wraplength=750, justify="center"
        )
        self.summary_label.pack()

        # Scrollable results output
        out_frame = tk.Frame(tab, bg=COLORS["bg"])
        out_frame.pack(fill="both", expand=True, padx=10, pady=(4, 0))

        self.results_text = scrolledtext.ScrolledText(
            out_frame,
            wrap=tk.WORD,
            font=("Courier New", 9),
            bg=COLORS["panel"],
            fg=COLORS["text"],
            relief="flat",
            borderwidth=1,
            padx=10, pady=8
        )
        self.results_text.pack(fill="both", expand=True)

        # Configure text tags for color-coded output
        self.results_text.tag_config("critical",    foreground=COLORS["critical"],  font=("Courier New", 9, "bold"))
        self.results_text.tag_config("warning",     foreground=COLORS["warning"],   font=("Courier New", 9, "bold"))
        self.results_text.tag_config("stable",      foreground=COLORS["stable"],    font=("Courier New", 9, "bold"))
        self.results_text.tag_config("section",     foreground=COLORS["accent"],    font=("Courier New", 10, "bold"))
        self.results_text.tag_config("label",       foreground=COLORS["subtext"],   font=("Courier New", 9, "bold"))
        self.results_text.tag_config("body",        foreground=COLORS["text"],      font=("Courier New", 9))
        self.results_text.tag_config("divider",     foreground=COLORS["border"])

    # ── Footer (Diagnose button + Clear) ──────────────────────────────────────
    def _build_footer(self):
        footer = tk.Frame(self.root, bg=COLORS["bg"], pady=10)
        footer.pack(fill="x", padx=16)

        tk.Button(
            footer,
            text="  🔍  Run Diagnosis  ",
            command=self._run_diagnosis,
            bg=COLORS["button"], fg=COLORS["button_text"],
            font=("Helvetica", 12, "bold"),
            relief="flat", cursor="hand2",
            padx=20, pady=8
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            footer,
            text="  ✖  Clear All  ",
            command=self._clear_all,
            bg=COLORS["border"], fg=COLORS["text"],
            font=("Helvetica", 10),
            relief="flat", cursor="hand2",
            padx=12, pady=8
        ).pack(side="left")

        tk.Label(
            footer,
            text="Knowledge source: NAQDA · NARA · FAO Aquaculture Guidelines",
            font=("Helvetica", 8), fg=COLORS["subtext"],
            bg=COLORS["bg"]
        ).pack(side="right")

    # ── Core: Run Diagnosis ───────────────────────────────────────────────────
    def _run_diagnosis(self):
        species = self.species_var.get()

        # Parse water params — skip blank fields
        water_params = {}
        for key, var in self.water_vars.items():
            val = var.get().strip()
            if val:
                try:
                    water_params[key] = float(val)
                except ValueError:
                    self._show_error(f"Invalid value for {key}: '{val}' — must be a number.")
                    return

        # Collect behavior symptoms
        behavior = [k for k, var in self.behavior_vars.items() if var.get()]

        # Collect physical symptoms with location
        physical = [
            (k, loc)
            for k, loc, _ in PHYSICAL_SYMPTOMS
            if self.physical_vars[k].get()
        ]

        # Pond metadata
        pond_age = None
        if self.pond_age_var.get().strip():
            try:
                pond_age = int(self.pond_age_var.get().strip())
            except ValueError:
                pass

        # Guard: need at least some input
        if not water_params and not behavior and not physical:
            self._show_error("Please enter at least one water reading or select one symptom.")
            return

        # Run the engine
        result = run_full_diagnosis(
            species            = species,
            water_params       = water_params,
            behavior_symptoms  = behavior,
            physical_symptoms  = physical,
            pond_age_days      = pond_age,
            stocking_density   = self.stocking_var.get()
        )

        # Switch to results tab and render
        self.nb.select(3)
        self._render_results(result)

    # ── Render Results ────────────────────────────────────────────────────────
    def _render_results(self, result: dict):
        t = self.results_text
        t.config(state="normal")
        t.delete("1.0", tk.END)

        status = result["overall_status"]
        color_tag = status.lower()  # "critical" | "warning" | "stable"

        # Update status banner
        status_colors = {
            "Critical": (COLORS["critical"], COLORS["critical_bg"]),
            "Warning" : (COLORS["warning"],  COLORS["warning_bg"]),
            "Stable"  : (COLORS["stable"],   COLORS["stable_bg"]),
        }
        fg, bg = status_colors.get(status, (COLORS["text"], COLORS["bg"]))
        self.status_label.config(
            text=f"● {status.upper()}",
            fg=fg, bg=bg
        )
        self.summary_label.config(text=result["summary"], bg=bg)
        self.status_frame.config(bg=bg)

        # ── Water Alerts ─────────────────────────────────────────────────────
        t.insert(tk.END, "━" * 62 + "\n", "divider")
        t.insert(tk.END, " 💧  WATER QUALITY ALERTS\n", "section")
        t.insert(tk.END, "━" * 62 + "\n", "divider")

        if result["water_alerts"]:
            for alert in result["water_alerts"]:
                lvl = alert["level"].upper()
                tag = "critical" if lvl == "CRITICAL" else "warning"
                t.insert(tk.END, f"\n  [{lvl}] {alert['parameter'].upper()}", tag)
                t.insert(tk.END, f"  —  Measured: {alert['actual']}  |  Safe range: {alert['safe_range']}\n", "body")
                t.insert(tk.END, f"  Correction: {alert['correction']}\n", "body")
        else:
            t.insert(tk.END, "\n  ✅  All water parameters within safe range.\n", "stable")

        # ── Disease Diagnoses ─────────────────────────────────────────────────
        t.insert(tk.END, "\n" + "━" * 62 + "\n", "divider")
        t.insert(tk.END, " 🦠  DISEASE DIAGNOSES\n", "section")
        t.insert(tk.END, "━" * 62 + "\n", "divider")

        if result["diagnoses"]:
            for i, diag in enumerate(result["diagnoses"], 1):
                urg = diag["urgency"]
                urg_tag = "critical" if urg == "Immediate" else (
                           "warning" if urg == "Within 24hrs" else "stable")

                t.insert(tk.END, f"\n  [{i}] {diag['disease']}\n", "section")
                t.insert(tk.END,  "  Cause      : ", "label")
                t.insert(tk.END,  diag["cause"] + "\n", "body")
                t.insert(tk.END,  "  Confidence : ", "label")
                t.insert(tk.END,  diag["confidence"] + "\n", "body")
                t.insert(tk.END,  "  Urgency    : ", "label")
                t.insert(tk.END,  urg + "\n", urg_tag)
                t.insert(tk.END,  "  Treatment  :\n", "label")
                for line in diag["treatment"].split("\n"):
                    t.insert(tk.END, f"    {line}\n", "body")
                t.insert(tk.END,  "  Prevention :\n", "label")
                t.insert(tk.END,  f"    {diag['prevention']}\n", "body")
                t.insert(tk.END,  "  " + "─" * 58 + "\n", "divider")
        else:
            t.insert(tk.END, "\n  ✅  No disease patterns matched. Monitor pond closely.\n", "stable")

        t.config(state="disabled")

    # ── Clear All ─────────────────────────────────────────────────────────────
    def _clear_all(self):
        for var in self.water_vars.values():
            var.set("")
        for var in self.behavior_vars.values():
            var.set(False)
        for var in self.physical_vars.values():
            var.set(False)
        self.pond_age_var.set("")
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.config(state="disabled")
        self.status_label.config(text="Run a diagnosis to see results.",
                                 fg=COLORS["subtext"], bg=COLORS["bg"])
        self.summary_label.config(text="", bg=COLORS["bg"])
        self.status_frame.config(bg=COLORS["bg"])
        self.nb.select(0)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _make_tab(self, title: str) -> tk.Frame:
        frame = tk.Frame(self.nb, bg=COLORS["bg"])
        self.nb.add(frame, text=title)
        return frame

    def _section(self, parent, title: str) -> tk.Frame:
        wrapper = tk.Frame(parent, bg=COLORS["bg"])
        wrapper.pack(fill="x", padx=10, pady=8)
        tk.Label(
            wrapper, text=title,
            font=("Helvetica", 10, "bold"),
            bg=COLORS["bg"], fg=COLORS["accent"]
        ).pack(anchor="w", pady=(0, 4))
        panel = tk.Frame(wrapper, bg=COLORS["panel"],
                         relief="flat", bd=1,
                         highlightbackground=COLORS["border"],
                         highlightthickness=1)
        panel.pack(fill="x")
        return panel

    def _show_error(self, msg: str):
        top = tk.Toplevel(self.root)
        top.title("Input Error")
        top.geometry("360x120")
        top.configure(bg=COLORS["bg"])
        tk.Label(top, text=msg, wraplength=320,
                 bg=COLORS["bg"], fg=COLORS["critical"],
                 font=("Helvetica", 10)).pack(pady=20)
        tk.Button(top, text="OK", command=top.destroy,
                  bg=COLORS["accent"], fg="white",
                  relief="flat", padx=16).pack()