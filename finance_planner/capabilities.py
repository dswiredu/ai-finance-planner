"""
Capability registry for the Finance Analytics Planner.

This file defines WHAT the system supports.
No AI. No execution. No side effects.
"""

from typing import Dict, Set


# -----------------------------
# Supported Metrics
# -----------------------------

SUPPORTED_METRICS: Set[str] = {
    "daily_pnl",
    "rolling_volatility",
    # "cumulative_pnl",  # intentionally commented out for now
}


# -----------------------------
# Supported Data Sources
# -----------------------------

SUPPORTED_DATA_SOURCES: Set[str] = {
    "positions",
}


# -----------------------------
# Supported Filters and Operators
# -----------------------------

SUPPORTED_FILTERS: Dict[str, Set[str]] = {
    "portfolio_id": {"="},
    "date": {"between", "=", ">=", "<="},
}


# -----------------------------
# Supported Visualization Types
# -----------------------------

SUPPORTED_VISUALIZATIONS: Set[str] = {
    "line",
}


# -----------------------------
# Governance Thresholds
# -----------------------------

HIGH_IMPACT_ASSUMPTIONS = {
    "high",
}


# -----------------------------
# Helper Functions
# -----------------------------

def is_metric_supported(metric_name: str) -> bool:
    return metric_name in SUPPORTED_METRICS


def is_data_source_supported(source_name: str) -> bool:
    return source_name in SUPPORTED_DATA_SOURCES


def is_filter_supported(field: str, operator: str) -> bool:
    return operator in SUPPORTED_FILTERS.get(field, set())


def is_visualization_supported(chart_type: str) -> bool:
    return chart_type in SUPPORTED_VISUALIZATIONS
