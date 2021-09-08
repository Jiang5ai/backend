from app_common.utils.base_view import BaseViewSet
from app_api.models import TestCase
from app_api.serializer import CaseSerializer, CaseValidator
from rest_framework.decorators import action
from app_common.utils.pagination import Pagination


class CaseViewSet(BaseViewSet):
    queryset = TestCase.objects.all()
    serializer_class = CaseSerializer
    authentication_classes = []

    @action(methods=['get'], detail=True, url_path='info')
    def get_case_info(self, request, *args, **kwargs):
        """
        获取一条用例信息
        api/v1/case/<case_id>info
        """
        cid = kwargs.get("pk", "")
        try:
            project = TestCase.objects.get(pk=cid)
            ser = CaseSerializer(instance=project, many=False)
        except (TestCase.DoesNotExist, ValueError):
            return self.response(error=self.CASE_ID_NULL)
        return self.response(data=ser.data)

    @action(methods=['get'], detail=False, url_path='list')
    def get_case_list(self, request, *args, **kwargs):
        """
        获取用例列表
        api/v1/case/list
        """
        page = request.query_params.get("page", 1)
        size = request.query_params.get("size", 5)
        case = TestCase.objects.filter(is_delete=False)
        pg = Pagination()
        page_data = pg.paginate_queryset(queryset=case, request=request, view=self)
        ser = CaseSerializer(instance=page_data, many=True)
        data = {
            "total": len(case),
            "page": int(page),
            "size": int(size),
            "projectList": ser.data,
        }
        return self.response(data=data)

    @action(methods=['post'], detail=False, url_path='create')
    def create_case(self, request, *args, **kwargs):
        """
        创建一条用例
        api/v1/case/create
        {
        "module_id":1,
        "name":"testcase1",
        "url":"http://httpbin.org/post",
        "method":"POST",
        "params_type":"form",
        "params_body":"{'key':'interface'}",
        "assert_type":"equal",
         "result":"post interface",
        "assert_text":"httpbin.org"
        }
        """
        val = CaseValidator(data=request.data)  # 获取参数传进验证器

        if val.is_valid():
            """判断验证器字段是否通过"""
            val.save()
        else:
            return self.response_fail(error=val.errors)

        return self.response(data=val.data)

    @action(methods=['put'], detail=True, url_path='update')
    def update_case(self, request, *args, **kwargs):
        """
        更新一条用例
        api/v1/case/<pk>/update
        """
        cid = kwargs.get('pk', '')
        try:
            case = TestCase.objects.get(pk=cid, is_delete=False)
        except (TestCase.DoesNotExist, ValueError):
            return self.response(error=self.CASE_ID_NULL)
        # 更新操作
        val = CaseValidator(instance=case, data=request.data)
        if val.is_valid():
            """判断验证器字段是否通过"""
            val.save()
            return self.response(data=val.data)
        else:
            return self.response_fail(error=val.errors)

    @action(methods=["delete"], detail=True, url_path='delete')
    def delete_case(self, request, *args, **kwargs):
        """
        删除一条用例
        api/v1/case/<pk>/delete
        """
        cid = kwargs.get("pk", "")
        try:
            case = TestCase.objects.filter(pk=cid).update(is_delete=1)
            if case == 0:
                return self.response_fail(error=self.CASE_DELETE_ERROR)
            return self.response()
        except (TestCase.DoesNotExist, ValueError):
            return self.response(error=self.CASE_ID_NULL)

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
        return self.response()
