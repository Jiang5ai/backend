from app_common.utils.base_view import BaseViewSet
from app_api.models import TestTask, TestResult
from app_api.serializer import CaseSerializer, CaseValidator, DebugValidator, AssertValidator, AssertType
from rest_framework.decorators import action
from app_api.tasks import running
from app_common.utils.pagination import Pagination
import requests
import json


class TaskViewSet(BaseViewSet):
    queryset = TestTask.objects.all()
    authentication_classes = []

    @action(methods=["get"], detail=True, url_path='running')
    def get_running(self, request, *args, **kwargs):
        """
        运行测试任务
        /api/interface/v1/task/<pk>/running/
        todo:
        1.记录任务状态
        2.读取xml文件的内容，写入表
        """
        pk = kwargs.get("pk")
        if pk is not None:
            try:
                task = TestTask.objects.get(id=pk, is_delete=False)
            except TestTask.DoesNotExist:
                pass
        running.delay()
        return self.response()
