# Architecture

- **Service**: FastAPI single service (can be embedded as microservice)
- **Contract**: `openapi.yaml` (source of truth)
- **Build/Release**: GitHub Actions (tag → release + ZIP)
- **Methodology**: See the Notion page → https://www.notion.so/266eb70eb32f8089b1d9d456506aad8d

## Future
- Plug ML models for symptom triage & lifestyle clustering
- Logging & privacy controls
- Localization (UA/RU/EN)
# Архітектура модуля (повна)

- **Вхід**: {age?, sex?, symptoms[], lifestyle?, notes?}
- **Пайплайн**: safety (red_flags) → scoring (risk_scoring) → mapping (mapping) → merge(plan)
- **Вихід**: {escalate, reason?, risks[], plan[], disclaimer}
- **Дані**: YAML у `data/rules/*`, `data/protocols/*`
- **API**: POST /v1/assessment, GET /v1/protocols/{id}, POST /v1/feedback
- **Етика/безпека**: decision‑support, не медичний виріб
