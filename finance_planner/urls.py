from django.urls import path

from .views import generate_finance_plan


urlpatterns = [
    path("plan/", generate_finance_plan, name="generate_finance_plan"),
]
