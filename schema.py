from typing import List, Optional, Literal
from pydantic import BaseModel, Field


# -----------------------------
# 1. High-Level Intent
# -----------------------------

class AnalyticsIntent(BaseModel):
    summary: str = Field(..., description="One-sentence business-facing description of the analytics request")
    domain: Literal[
        "portfolio_analytics",
        "risk",
        "performance",
    ]


# -----------------------------
# 2. Metrics
# -----------------------------

class MetricDefinition(BaseModel):
    name: Literal[
        "daily_pnl",
        "cumulative_pnl",
        "rolling_volatility",
    ]
    description: str
    frequency: Literal["daily"]
    unit: Literal["currency", "percentage"]


# -----------------------------
# 3. Data Sources
# -----------------------------

class DataSource(BaseModel):
    name: Literal[
        "positions",
        "prices",
        "trades",
        "market_data",
    ]
    granularity: Literal["daily"]
    required_fields: List[str]


# -----------------------------
# 4. Calculations
# -----------------------------

class CalculationStep(BaseModel):
    step_id: int = Field(..., ge=1)
    description: str
    depends_on: List[int] = Field(default_factory=list)


# -----------------------------
# 5. Filters
# -----------------------------

class FilterDefinition(BaseModel):
    field: Literal[
        "portfolio_id",
        "date",
    ]
    operator: Literal["=", "between"]
    required: bool


# -----------------------------
# 6. API Outputs
# -----------------------------

class APIOutput(BaseModel):
    name: str
    type: Literal["time_series"]
    fields: List[str]


# -----------------------------
# 7. Visualizations
# -----------------------------

class Visualization(BaseModel):
    chart_type: Literal["line"]
    x_axis: str
    y_axis: str
    series: Optional[str] = None


# -----------------------------
# 8. Assumptions
# -----------------------------

class Assumption(BaseModel):
    description: str
    impact: Literal["low", "medium", "high"]


# -----------------------------
# 9. Risks & Constraints
# -----------------------------

class Risk(BaseModel):
    description: str
    mitigation: str


# -----------------------------
# 10. Top-Level Plan Object
# -----------------------------

class FinanceAnalyticsPlan(BaseModel):
    intent: AnalyticsIntent
    metrics: List[MetricDefinition]
    data_sources: List[DataSource]
    calculations: List[CalculationStep]
    filters: List[FilterDefinition]
    api_outputs: List[APIOutput]
    visualizations: List[Visualization]
    assumptions: List[Assumption]
    risks: List[Risk]
