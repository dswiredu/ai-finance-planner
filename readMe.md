A production-grade AI planning component that converts natural language finance analytics requests into a validated, governable execution plan — without executing anything.

- Accepts natural-language analytics requests:
```
“Create a dashboard that shows daily portfolio PnL and rolling 30-day volatility…”
```

- Converts them into a typed, structured plan
```
FinanceAnalyticsPlan
```

- Enforces a finite analytics vocabulary
    - metrics
    - filters
    - data sources
    - visualizations

- Separates concerns cleanly
    - AI → interpretation only
    - Code → permission & governance
    - No execution leakage

- Returns a decision artifact:
```
{
  "plan": {...},
  "validation": {...}
}
```

This is a Reusable template (at least for finance apps).
Every future Django + AI feature you build can follow this exact shape:
```
HTTP Boundary
    ↓
AI Planner (LLM + schema)
    ↓
Typed Intent Object (Pydantic)
    ↓
Capability / Policy Validation (Code)
    ↓
Decision Artifact
```

- Only two things change per project:
    - the schema
    - the capabilities

- In future projects, you can literally copy:
    - views.py pattern
    - llm.py pattern (planner only)
    - validation.py pattern
    - capability registry pattern
    - error handling pattern
    - And just change:
        - schema
        - prompt
        - capabilities
That’s a template.

If want to build a mental and technical model for using AI safely, deterministically, and productively in finance systems then this project is meant to become your default starting point for any serious Django + AI feature going forward.