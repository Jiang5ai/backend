from django.urls import path
from app_api.views.project_views import ProjectView
from app_api.views.module_views import ModuleView

urlpatterns = [
    path('v1/project/', ProjectView.as_view()),
    path('v1/module/', ModuleView.as_view()),
]
