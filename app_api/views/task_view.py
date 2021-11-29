import os
import json
from app_common.utils.base_view import BaseViewSet
from app_api.models import TestTask, TestCase
from app_api.serializer import TaskValidator, TaskSerializer
from rest_framework.decorators import action
from app_api.tasks import running
from backend.settings import BASE_DIR
from app_common.utils.pagination import Pagination
from app_api.task_thread import TaskThread

DATA_FILE_PATH = os.path.join(BASE_DIR, "app_api", "data", "test_data.json")


class TaskViewSet(BaseViewSet):
    queryset = TestTask.objects.all()
    authentication_classes = []

    @action(methods=["get"], detail=True, url_path='info')
    def get_task_info(self, request, *args, **kwargs):
        """
        查询测试任务
        /api/v1/task/<pk>/info/
        """
        tid = kwargs.get("pk", "")
        try:
            task = TestTask.objects.get(pk=tid, is_delete=False)
            ser = TaskSerializer(instance=task, many=False)
        except (TestCase.DoesNotExist, ValueError):
            return self.response(error=self.TASK_ID_NULL)
        return self.response(data=ser.data)

    @action(methods=['get'], detail=False, url_path='list')
    def get_task_list(self, request, *args, **kwargs):
        """
        获取测试任务列表
        api/v1/task/list
        """
        page = request.query_params.get("page", 1)
        size = request.query_params.get("size", 5)
        task = TestTask.objects.filter(is_delete=False)
        pg = Pagination()
        page_data = pg.paginate_queryset(queryset=task, request=request, view=self)
        ser = TaskSerializer(instance=page_data, many=True)
        data = {
            "total": len(task),
            "page": int(page),
            "size": int(size),
            "taskList": ser.data,
        }
        return self.response(data=data)

    @action(methods=["post"], detail=False, url_path='create')
    def create_task(self, request, *args, **kwargs):
        """
        创建测试任务
        /api/v1/task/create/
        """
        val = TaskValidator(data=request.data)
        if val.is_valid():
            val.save()
        else:
            return self.response_fail(error=val.errors)

        return self.response(data=val.data)

    @action(methods=["delete"], detail=True, url_path='delete')
    def delete_task(self, request, *args, **kwargs):
        """
        删除一条测试任务
        api/v1/task/<pk>/delete
        """
        cid = kwargs.get("pk", "")
        try:
            case = TestTask.objects.filter(pk=cid).update(is_delete=1)
            if case == 0:
                return self.response_fail(error=self.TASK_DELETE_ERROR)
            return self.response()
        except (TestTask.DoesNotExist, ValueError):
            return self.response(error=self.TASK_DELETE_ERROR)

    @action(methods=["post"], detail=True, url_path='update')
    def update_task(self, request, *args, **kwargs):
        """
        更新一条测试任务
        api/v1/task/<pk>/update
        """
        tid = kwargs.get('pk', '')
        try:
            task = TestTask.objects.get(pk=tid, is_delete=False)
        except (TestTask.DoesNotExist, ValueError):
            return self.response(error=self.TASK_ID_NULL)
        # 更新操作
        val = TaskValidator(instance=task, data=request.data)
        if val.is_valid():
            """判断验证器字段是否通过"""
            val.save()
            return self.response(data=val.data)
        else:
            return self.response_fail(error=val.errors)

    @action(methods=["get"], detail=True, url_path='running')
    def get_running(self, request, *args, **kwargs):
        """
        运行测试任务
        /api/interface/v1/task/<pk>/running/
        """
        tid = kwargs.get("pk")
        if tid is not None:
            try:
                task = TestTask.objects.get(pk=tid, is_delete=False)
                ser = TaskSerializer(instance=task, many=False)
            except TestTask.DoesNotExist:
                return self.response(error=self.TASK_OBJECT_NULL)

            case_list = ser.data.get("cases", [])
            # running.delay()
            TaskThread(tid, case_list).run()
            print("case list-->", case_list)

        return self.response()

