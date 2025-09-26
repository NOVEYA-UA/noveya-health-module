from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter()

# ---- Request / Response ----
class AssessmentRequest(BaseModel):
    age: Optional[int] = Field(None, ge=0, description="Age in years")
    sex: Optional[str] = None
    symptoms: List[str] = Field(default_factory=list)
    lifestyle: Optional[str] = None
    notes: Optional[str] = None

class AssessmentResponse(BaseModel):
    # добавили поле escalate и план от движка,
    # при fallback они останутся пустыми/False
    escalate: bool = False
    risks: List[str] = []
    suggestions: List[str] = []
    plan: List[dict] = []
    disclaimer: str = "Not a medical device. Educational/decision-support only."

# ---- Пытаемся подключить движок; если нет — используем fallback ----
USE_ENGINE = True
try:
    from ..core.engine import assess as engine_assess  # app/core/engine.py
except Exception:
    USE_ENGINE = False

@router.post("/assessment", response_model=AssessmentResponse)
def assess_endpoint(req: AssessmentRequest):
    s = [x.lower() for x in (req.symptoms or [])]

    if USE_ENGINE:
        try:
            result = engine_assess(s)
            return AssessmentResponse(
                escalate=bool(result.get("escalate", False)),
                risks=result.get("risks", []),
                plan=result.get("plan", []),
            )
        except Exception:
            # Если движок есть, но что-то упало — тихо откатываемся к эвристикам
            pass

    # ----- Fallback: прежняя логика эвристик -----
    risks: List[str] = []
    suggestions: List[str] = []

    if "headache" in s or "головний біль" in s:
        risks.append("Possible dehydration or tension-related headache")
        suggestions += [
            "Hydration check and rest",
            "Consider posture/vision ergonomics",
            "Consult a clinician if persistent or severe",
        ]
    if "burnout" in s or "виснаження" in s:
        risks.append("Psychosocial stress / burnout risk")
        suggestions += ["Sleep hygiene", "Light activity", "Mindfulness / counseling"]

    if not risks:
        suggestions.append("No specific risk rules fired; consider preventive checkup.")

    return AssessmentResponse(risks=risks, suggestions=suggestions)

@router.get("/recommendations")
def recommendations(category: str = "general") -> dict:
    baseline = [
        "Balanced nutrition & hydration",
        "Regular movement and sleep routine",
        "Periodic medical checkups",
        "Energy & attention hygiene (digital breaks, breathing)",
    ]
    return {"category": category, "recommendations": baseline}
