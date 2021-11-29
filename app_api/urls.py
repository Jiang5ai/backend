from django.urls import path
from app_api.views.project_views import ProjectView,ProjectModuleView
from app_api.views.module_views import ModuleView
from app_api.views.case_views import CaseViewSet
from app_api.views.task_view import TaskViewSet
from rest_framework import routers

url_path = [
    path('v1/project/', ProjectView.as_view()),
    path('v1/project/<int:pk>/', ProjectView.as_view()),
    path('v1/project/<int:pk>/module/', ProjectModuleView.as_view()),
    path('v1/module/', ModuleView.as_view()),
    path('v1/module/<int:pk>/', ModuleView.as_view()),
]
router = routers.SimpleRouter()
router.register(r'v1/case', CaseViewSet)
router.register(r'v1/task', TaskViewSet)
urlpatterns = url_path + router.urls
