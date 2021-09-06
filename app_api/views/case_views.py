from app_common.utils.base_view import BaseViewSet
from app_api.models import Project
from app_api.serializer.project import ProjectSerializer
from rest_framework.decorators import action
from app_common.utils.response import response


class CaseViewSet(BaseViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = []

    @action(methods=['get'], detail=True, url_path='info')
    def get_case_info(self, request, *args, **kwargs):
        """
        获取一条用例信息
        api/v1/case/<case_id>info
        """
        return self.response()

    @action(methods=['get'], detail=False, url_path='list')
    def get_case_list(self, request, *args, **kwargs):
        """
        获取用例列表
        api/v1/case/list
        """
        return self.response()

    @action(methods=['post'], detail=False, url_path='create')
    def create_case(self, request, *args, **kwargs):
        """
        创建一条用例
        api/v1/case/create
        """
        return self.response()

    @action(methods=['put'], detail=True, url_path='update')
    def update_case(self, request, *args, **kwargs):
        """
        更新一条用例
        api/v1/case/<pk>/update
        """
        return self.response()

    @action(methods=["delete"], detail=True, url_path='delete')
    def delete_case(self, request, *args, **kwargs):
        """
        删除一条用例
        api/v1/case/<pk>/delete
        """
        return self.response()

    @action(methods=["post"], detail=False, url_path='debug')
    def debug_case(self, request, *args, **kwargs):
        """
        调试用例
        api/v1/case/debug
        """
        return self.response()

    @action(methods=["post"], detail=False, url_path='assert')
    def assert_case(self, request, *args, **kwargs):
        """
        调试用例
        api/v1/case/debug
        """
        return self.response()

    @action(methods=["get"], detail=False, url_path="tree")
    def get_case_tree(self, request, *args, **kwargs):
        """
        获取用例树；项目 -> 模块 -> 用例
        """
        print(request)
        print(args)
        print(kwargs)
        return response()
