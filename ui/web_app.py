from flask import Flask, render_template, request

from engine.master_engine import run_full_diagnosis
from ui.options import BEHAVIOR_SYMPTOMS, PHYSICAL_SYMPTOMS, WATER_FIELDS


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        form_data = _default_form_data()
        result = None
        error = None

        if request.method == "POST":
            form_data = _read_form_data(request.form)
            error, result = _run_web_diagnosis(form_data)

        return render_template(
            "index.html",
            behavior_symptoms=BEHAVIOR_SYMPTOMS,
            physical_symptoms=PHYSICAL_SYMPTOMS,
            water_fields=WATER_FIELDS,
            form=form_data,
            result=result,
            error=error,
        )

    return app


def run_web_app(host="127.0.0.1", port=5000, debug=False):
    app = create_app()
    app.run(host=host, port=port, debug=debug)


def _default_form_data():
    return {
        "species": "shrimp",
        "pond_age_days": "",
        "stocking_density": "medium",
        "water_params": {key: "" for key, _, _ in WATER_FIELDS},
        "behavior_symptoms": [],
        "physical_symptoms": [],
    }


def _read_form_data(form):
    return {
        "species": form.get("species", "shrimp"),
        "pond_age_days": form.get("pond_age_days", "").strip(),
        "stocking_density": form.get("stocking_density", "medium"),
        "water_params": {
            key: form.get(key, "").strip()
            for key, _, _ in WATER_FIELDS
        },
        "behavior_symptoms": form.getlist("behavior_symptoms"),
        "physical_symptoms": form.getlist("physical_symptoms"),
    }


def _run_web_diagnosis(form_data):
    water_params = {}
    for key, value in form_data["water_params"].items():
        if value:
            try:
                water_params[key] = float(value)
            except ValueError:
                return f"Invalid value for {key}: '{value}' must be a number.", None

    pond_age = None
    if form_data["pond_age_days"]:
        try:
            pond_age = int(form_data["pond_age_days"])
        except ValueError:
            return "Days since stocking must be a whole number.", None

    behavior = form_data["behavior_symptoms"]
    physical_locations = {
        symptom: location
        for symptom, location, _ in PHYSICAL_SYMPTOMS
    }
    physical = [
        (symptom, physical_locations[symptom])
        for symptom in form_data["physical_symptoms"]
        if symptom in physical_locations
    ]

    if not water_params and not behavior and not physical:
        return "Please enter at least one water reading or select one symptom.", None

    result = run_full_diagnosis(
        species=form_data["species"],
        water_params=water_params,
        behavior_symptoms=behavior,
        physical_symptoms=physical,
        pond_age_days=pond_age,
        stocking_density=form_data["stocking_density"],
    )
    return None, result
