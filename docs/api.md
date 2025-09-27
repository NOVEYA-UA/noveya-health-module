# API — приклади використання

Локально: `http://localhost:8000`

## POST /v1/assessment
Тіло:
```json
{"symptoms":["інсулінорезистентність","жирова печінка"]}
```
Відповідь (приклад):
```json
{"escalate":false,"risks":["metabolic","nafld"],"plan":[{"proto":"insulin_resistance_v1","day_range":[1,14],"actions":["..."]}],"disclaimer":"Decision-support, not a medical device."}
```

## GET /v1/protocols/{id}
`/v1/protocols/insulin_resistance_v1` — повертає YAML.

## POST /v1/feedback
Зберігає рядок у `logs/feedback.jsonl`.
