@'
from __future__ import annotations
from pathlib import Path
import yaml

# Папка с YAML (repo_root/data)
DATA_DIR = Path(__file__).resolve().parents[2] / "data"

def _load(rel: str):
    p = DATA_DIR / rel
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def assess(symptoms: list[str]) -> dict:
    s = set([x.lower().strip() for x in (symptoms or [])])

    # 1) Красные флаги — немедленная эскалация
    red = _load("rules/red_flags.yaml")
    for crit in red.get("critical", []):
        if crit.lower() in s:
            return {"escalate": True, "reason": f"red_flag:{crit}", "risks": [], "plan": []}

    # 2) Скоринг рисков (простые правила; потом можно ML)
    scoring = _load("rules/risk_scoring.yaml")
    risks = []
    for rule in scoring.get("rules", []):
        if s.intersection([x.lower() for x in rule.get("if_any", [])]):
            risks.append(rule["risk"])

    # 3) Подбор протоколов под риски
    risk_to_protocols = {
        "burnout": ["burnout_baseline_v1"],
        "tension_headache": ["headache_tension_v1", "sleep_hygiene_v1", "hydration_v1"]
    }

    plan = []
    for r in risks:
        for proto_id in risk_to_protocols.get(r, []):
            yml = _load(f"protocols/{proto_id}.yaml")
            for step in yml.get("steps", []):
                plan.append({"proto": proto_id, **step})

    return {"escalate": False, "risks": risks, "plan": plan}
'@ | Set-Content -Encoding UTF8 app/core/engine.py
