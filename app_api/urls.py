from django.urls import path
from app_api.views.project_views import ProjectView
from app_api.views.module_views import ModuleView
from app_api.views.case_views import CaseViewSet
from rest_framework import routers

url_path = [
    path('v1/project/', ProjectView.as_view()),
    path('v1/module/', ModuleView.as_view()),
]
router = routers.SimpleRouter()
router.register(r'v1/case', CaseViewSet)
urlpatterns = url_path + router.urls
