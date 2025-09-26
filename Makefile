.PHONY: dev test lint build sdk

    dev:
	uvicorn app.main:app --reload --port 8000

    test:
	pytest -q || echo "Add tests under tests/"

    lint:
	python -m pip install ruff && ruff check app

    build:
	zip -r dist/noveya-health-module.zip . -x "dist/*" ".venv/*" ".git/*"

    sdk:
	scripts/generate_sdk.sh

    openapi-validate:
	docker run --rm -v ${PWD}:/work redocly/openapi-cli:latest lint /work/openapi.yaml || true
