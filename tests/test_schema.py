import pytest
from pydantic import ValidationError

from schema import FinanceAnalyticsPlan


def test_invalid_metric_name_raises_validation_error() -> None:
    """
    The schema must reject unknown / invented metric names.
    This is a critical invariant for finance correctness.
    """

    bad_payload = {
        "intent": {
            "summary": "Test invalid metric",
            "domain": "portfolio_analytics",
        },
        "metrics": [
            {
                "name": "made_up_metric",
                "description": "This metric should not exist",
                "frequency": "daily",
                "unit": "currency",
            }
        ],
        "data_sources": [],
        "calculations": [],
        "filters": [],
        "api_outputs": [],
        "visualizations": [],
        "assumptions": [],
        "risks": [],
    }

    with pytest.raises(ValidationError):
        FinanceAnalyticsPlan.model_validate(bad_payload)
