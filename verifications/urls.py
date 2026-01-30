from django.urls import path
from .views import (
    PassportVerificationCreateView,
    PassportVerificationDetailView,
)

urlpatterns = [
    path("verifications/", PassportVerificationCreateView.as_view()),
    path("verifications/<uuid:pk>/", PassportVerificationDetailView.as_view()),
]