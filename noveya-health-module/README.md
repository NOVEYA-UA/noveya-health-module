# NOVEYA • AI Health Module (Integrative Medicine)

> Комплексна методологія інтегративної медицини. ШІ‑модуль здоров'я.
>
> Орієнтир (джерело методології): [https://www.notion.so/266eb70eb32f8089b1d9d456506aad8d](https://www.notion.so/266eb70eb32f8089b1d9d456506aad8d)

## 🚀 Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/docs

## 📦 Releases

Push a tag like `v0.1.0` and GitHub Actions will create a release with a packaged ZIP.

## 📚 Structure

- `app/` — FastAPI service: endpoints for assessment & recommendations
- `openapi.yaml` — API contract (source of truth). SDKs are generated from this.
- `scripts/generate_sdk.sh` — SDK generation via OpenAPI Generator (Docker).
- `docs/` — Architecture notes, links to the methodology page
- `.github/workflows/release.yml` — tag → release + asset upload
- `Dockerfile.dev` — dev container with hot reload
- `SECURITY.md` — reporting vulnerabilities & PGP

## ⚖️ Ethics & Scope

This is **not** a medical device. Outputs are for education/decision‑support,
not diagnosis or treatment. Always seek qualified medical professionals.

## 🔗 Methodology Reference

- UA: “Здоров’я — Комплексна методологія інтегративного медицини ШІ‑модуля здоров'я” → https://www.notion.so/266eb70eb32f8089b1d9d456506aad8d
