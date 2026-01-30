from django.urls import path
from .views import (
    PassportRetryVerificationCreateView,
    PassportVerificationCreateView,
    PassportVerificationDetailView,
)

urlpatterns = [
    path("start-verifications", PassportVerificationCreateView.as_view()),
    path("retry-verifications/<uuid:pk>", PassportRetryVerificationCreateView.as_view()),
    path("verifications/<uuid:pk>", PassportVerificationDetailView.as_view()),
]