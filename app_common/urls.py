from django.urls import path
from app_common.views import LoginView

urlpatterns = [
    path('v1/login/', LoginView.as_view()),
]
