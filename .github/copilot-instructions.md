# Copilot Instructions

## Build, test, and lint commands

Use the repository virtual environment (`expert_env`) for all commands.

```bash
source expert_env/bin/activate
```

Run the available test scripts:

```bash
# Run all current checks
./expert_env/bin/python test_experta.py && ./expert_env/bin/python test_water.py

# Run a single test script
./expert_env/bin/python test_water.py
# or
./expert_env/bin/python test_experta.py
```

There is currently no build system or lint configuration committed in this repository (no Makefile, pyproject/tool config, or lint runner).

## High-level architecture

The project is an Experta-based expert system centered on rule-driven water-quality diagnosis:

1. **Domain fact model (`knowledge_base/facts.py`)**: Defines strongly-typed Fact classes grouped by lifecycle:
   - Input facts from UI/sensors (`FarmContext`, `WaterQuality`, `BehaviorSymptom`, `PhysicalSymptom`)
   - Intermediate facts from sub-engines (`WaterAlert`)
   - Final diagnosis facts (`DiseaseDiagnosis`, `SystemConclusion`)
2. **Rule engine (`knowledge_base/water_rules.py`)**: `WaterQualityEngine(KnowledgeEngine)` declares species-specific and shared rules that emit `WaterAlert` facts with actionable correction text.
3. **Execution entrypoints (current state)**:
   - `test_water.py` shows the intended inference flow (reset engine → declare context/readings → run → iterate emitted `WaterAlert`s).
   - `test_experta.py` is a framework smoke test.
   - `main.py`, `ui/app.py`, `engine/master_engine.py`, and disease rule files are placeholders (currently empty), so active behavior is concentrated in `facts.py` and `water_rules.py`.

## Key codebase conventions

- **Species values are canonical strings**: use `"tilapia"` or `"shrimp"` in `FarmContext(species=...)`; rules depend on exact matches.
- **Rule priority uses salience levels** in `water_rules.py`: critical conditions are written with higher salience than warning conditions so urgent alerts fire first.
- **Alert contract is stable and structured**: rules emit `WaterAlert` with `parameter`, `level`, `actual`, `safe_range`, `correction`; downstream consumers should read these keys rather than parsing free text.
- **Rule naming pattern is semantic**: methods follow `<species_or_scope>_<parameter>_<severity>` (for example `shrimp_ammonia_critical`, `nitrite_warning`) to keep rule intent obvious.
- **Fact classes are separated by role, not by feature file**: add new observation/diagnosis concepts in `facts.py` first, then reference them from rule files.
