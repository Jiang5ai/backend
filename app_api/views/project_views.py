from app_common.utils.base_view import BaseAPIView
from app_api.serializer.project import ProjectValidator, ProjectSerializer
from app_api.models.project_models import Project
from app_common.utils.pagination import Pagination
from app_common.utils.token_auth import TokenAuthentication


# Create your views here.
class ProjectView(BaseAPIView):

    def get(self, request, *args, **kwargs):
        """
        查询
        """
        pid = request.data.get("id")
        page = request.query_params.get("page", 1)
        size = request.query_params.get("size", 5)
        if pid:  # 查一个
            try:
                project = Project.objects.get(pk=pid)
                ser = ProjectSerializer(instance=project, many=False)
            except Project.DoesNotExist:
                return self.response(error=self.PROJECT_ID_NULL)
            return self.response(data=ser.data)
        else:  # 查一组
            project = Project.objects.filter(is_delete=False)
            pg = Pagination()
            page_data = pg.paginate_queryset(queryset=project, request=request, view=self)
            ser = ProjectSerializer(instance=page_data, many=True)
            data = {
                "total": len(project),
                "page": int(page),
                "size": int(size),
                "moduleList": ser.data,
            }
            return self.response(data=data)

    def post(self, request, *args, **kwargs):
        """
        添加

        """
        val = ProjectValidator(data=request.data)  # 获取参数传进验证器

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
        pid = request.data.get("id")
        if pid is None:
            return self.response_fail(error=self.PROJECT_ID_NULL)
        try:
            project = Project.objects.get(pk=pid, is_delete=False)
        except Project.DoesNotExist:
            return self.response_fail(error=self.PROJECT_OBJECT_NULL)

        # 更新操作
        val = ProjectValidator(instance=project, data=request.data)
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
        pid = request.data.get("id")
        if pid:
            project = Project.objects.filter(pk=pid, is_delete=False).update(is_delete=True)
            if project == 0:
                return self.response_fail(error=self.PROJECT_DELETE_ERROR)

        return self.response()
