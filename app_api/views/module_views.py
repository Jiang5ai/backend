from app_api.models.module_models import Module
from app_api.serializer import ModuleSerializer, ModuleValidator
from app_common.utils.base_view import BaseAPIView
from app_common.utils.pagination import Pagination


# Create your views here.
class ModuleView(BaseAPIView):

    def get(self, request, *args, **kwargs):
        """
        查询
        """
        mid = kwargs.get("pk")
        page = request.query_params.get("page", 1)
        size = request.query_params.get("size", 5)
        if mid:  # 查一个
            try:
                module = Module.objects.get(pk=mid)
                ser = ModuleSerializer(instance=module, many=False)
            except Module.DoesNotExist:
                return self.response(error=self.MODULE_ID_NULL)
            return self.response(data=ser.data)
        else:  # 查一组
            module = Module.objects.filter(is_delete=False)
            pg = Pagination()
            page_data = pg.paginate_queryset(queryset=module, request=request, view=self)
            ser = ModuleSerializer(instance=page_data, many=True)
            data = {
                "total": len(module),
                "page": int(page),
                "size": int(size),
                "moduleList": ser.data,
            }
            return self.response(data=data)

    def post(self, request, *args, **kwargs):
        """
        添加
        {
        "project_id":1,
        "name":"模块1~",
        "describe":"模块描述~"
        }
        """
        val = ModuleValidator(data=request.data)  # 获取参数传进验证器

        if val.is_valid():
            """判断验证器字段是否通过"""
            val.save()
        else:
            return self.response_fail(error=val.errors)

        return self.response(data=val.data)

    def put(self, request, *args, **kwargs):
        """
        更新
        """
        mid = kwargs.get("id")
        if mid is None:
            return self.response_fail(error=self.MODULE_ID_NULL)
        try:
            project = Module.objects.get(pk=mid, is_delete=False)
        except Module.DoesNotExist:
            return self.response_fail(error=self.MODULE_OBJECT_NULL)

        # 更新操作
        val = ModuleValidator(instance=project, data=request.data)
        if val.is_valid():
            """判断验证器字段是否通过"""
            val.save()
            return self.response(data=val.data)
        else:
            return self.response_fail(error=val.errors)

    def delete(self, request, *args, **kwargs):
        """
        删除
        """
        mid = kwargs.get("pk")
        if mid:
            module = Module.objects.filter(pk=mid, is_delete=False).update(is_delete=True)
            if module == 0:
                return self.response_fail(error=self.MODULE_DELETE_ERROR)

        return self.response()
