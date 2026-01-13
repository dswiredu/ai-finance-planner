"""
Plan validation logic for the Finance Analytics Planner.

This module determines whether a FinanceAnalyticsPlan
is supported by the current system capabilities.

No AI. No execution. Deterministic only.
"""

from typing import List

from pydantic import BaseModel

from finance_planner.schema import FinanceAnalyticsPlan
from finance_planner.capabilities import (
    is_metric_supported,
    is_data_source_supported,
    is_filter_supported,
    is_visualization_supported,
    HIGH_IMPACT_ASSUMPTIONS,
)


class PlanValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]
    warnings: List[str]



def validate_plan(plan: FinanceAnalyticsPlan) -> PlanValidationResult:
    errors: List[str] = []
    warnings: List[str] = []

    # -----------------------------
    # Metrics
    # -----------------------------
    for metric in plan.metrics:
        if not is_metric_supported(metric.name):
            errors.append(f"Unsupported metric: {metric.name}")

    # -----------------------------
    # Data Sources
    # -----------------------------
    for source in plan.data_sources:
        if not is_data_source_supported(source.name):
            errors.append(f"Unsupported data source: {source.name}")

    # -----------------------------
    # Filters
    # -----------------------------
    for flt in plan.filters:
        if not is_filter_supported(flt.field, flt.operator):
            errors.append(
                f"Unsupported filter/operator combination: {flt.field} {flt.operator}"
            )

    # -----------------------------
    # Visualizations
    # -----------------------------
    for viz in plan.visualizations:
        if not is_visualization_supported(viz.chart_type):
            errors.append(f"Unsupported visualization type: {viz.chart_type}")

    # -----------------------------
    # Assumptions (Governance)
    # -----------------------------
    for assumption in plan.assumptions:
        if assumption.impact in HIGH_IMPACT_ASSUMPTIONS:
            warnings.append(
                f"High-impact assumption requires review: {assumption.description}"
            )

    return PlanValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
    )
