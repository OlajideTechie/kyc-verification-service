from django.urls import path
from .views import (
    PassportVerificationCreateView,
    PassportVerificationDetailView,
)

urlpatterns = [
    path("start-verifications", PassportVerificationCreateView.as_view()),
    path("verifications/<uuid:verification_id>", PassportVerificationDetailView.as_view()),
]