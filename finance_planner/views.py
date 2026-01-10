import json

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .llm import generate_plan

@csrf_exempt
@require_POST
def generate_finance_plan(request):
    """
    POST endpoint that accepts a natural-language finance analytics request
    and returns a validated FinanceAnalyticsPlan.

    Expected payload:
    {
        "request": "<natural language analytics request>"
    }
    """

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON payload")

    user_request = payload.get("request")

    if not isinstance(user_request, str) or not user_request.strip():
        return HttpResponseBadRequest("Field 'request' must be a non-empty string")

    try:
        plan = generate_plan(user_request)
    except Exception as exc:
        # Planner failure: invalid request or invalid LLM output
        return HttpResponseBadRequest(str(exc))

    return JsonResponse(plan.model_dump(), status=200)
