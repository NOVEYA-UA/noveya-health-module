# Architecture

- **Service**: FastAPI single service (can be embedded as microservice)
- **Contract**: `openapi.yaml` (source of truth)
- **Build/Release**: GitHub Actions (tag → release + ZIP)
- **Methodology**: See the Notion page → https://www.notion.so/266eb70eb32f8089b1d9d456506aad8d

## Future
- Plug ML models for symptom triage & lifestyle clustering
- Logging & privacy controls
- Localization (UA/RU/EN)
