import os
import json

from openai import OpenAI
from pydantic import ValidationError

from finance_planner.schema import FinanceAnalyticsPlan


_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt_template = """ 
 You are a finance analytics planner.

You must return ONLY a JSON object that EXACTLY matches this structure.
Do not omit fields. Do not rename fields. Do not add extra fields.
Do not include markdown or code fences.

JSON STRUCTURE (fill in values, keep keys exactly the same):

{
  "intent": {
    "summary": "",
    "domain": "portfolio_analytics"
  },
  "metrics": [
    {
      "name": "daily_pnl",
      "description": "",
      "frequency": "daily",
      "unit": "currency"
    }
  ],
  "data_sources": [
    {
      "name": "positions",
      "granularity": "daily",
      "required_fields": []
    }
  ],
  "calculations": [
    {
      "step_id": 1,
      "description": "",
      "depends_on": []
    }
  ],
  "filters": [
    {
      "field": "portfolio_id",
      "operator": "=",
      "required": true
    }
  ],
  "api_outputs": [
    {
      "name": "",
      "type": "time_series",
      "fields": []
    }
  ],
  "visualizations": [
    {
      "chart_type": "line",
      "x_axis": "",
      "y_axis": ""
    }
  ],
  "assumptions": [
    {
      "description": "",
      "impact": "low"
    }
  ],
  "risks": [
    {
      "description": "",
      "mitigation": ""
    }
  ]
}

Allowed metric names: daily_pnl, cumulative_pnl, rolling_volatility.

"""


def generate_plan(user_request: str) -> FinanceAnalyticsPlan:
    if not user_request or not user_request.strip():
        raise ValueError("user_request must be a non-empty string")

    response = _client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": prompt_template,
            },
            {
                "role": "user",
                "content": user_request,
            },
        ],
        temperature=0,
    )

    raw_text = response.output_text or ""

    # Defensive: reject markdown-wrapped output
    if raw_text.strip().startswith("```"):
        raise ValueError(f"LLM returned markdown, not JSON:\n{raw_text}")

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM did not return valid JSON:\n{raw_text}") from exc

    try:
        return FinanceAnalyticsPlan.model_validate(data)
    except ValidationError as exc:
        raise ValueError(
            f"LLM JSON did not conform to FinanceAnalyticsPlan:\n{data}"
        ) from exc
