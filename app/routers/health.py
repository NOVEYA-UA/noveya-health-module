from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter()

class AssessmentRequest(BaseModel):
    age: Optional[int] = Field(None, ge=0, description="Age in years")
    sex: Optional[str] = Field(None, description="biological sex or self‑identified")
    symptoms: List[str] = Field(default_factory=list)
    lifestyle: Optional[str] = None
    notes: Optional[str] = None

class AssessmentResponse(BaseModel):
    risks: List[str] = []
    suggestions: List[str] = []
    disclaimer: str = "Not a medical device. Educational/decision-support only."

@router.post("/assessment", response_model=AssessmentResponse)
def assess(req: AssessmentRequest):
    risks, suggestions = [], []

    # toy heuristic rules — replace with proper models later
    s = [x.lower() for x in req.symptoms]
    if "headache" in s or "головний біль" in s:
        risks.append("Possible dehydration or tension-related headache")
        suggestions += [
            "Hydration check and rest",
            "Consider posture/vision ergonomics",
            "Consult a clinician if persistent or severe"
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
        "Energy & attention hygiene (digital breaks, breathing)"
    ]
    return {"category": category, "recommendations": baseline}
