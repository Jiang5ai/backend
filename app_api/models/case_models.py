from django.db import models
from app_api.models import Module


class TestCase(models.Model):
    """
    测试用例表
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100, null=False)
    url = models.TextField("URL", null=False)
    method = models.CharField("请求方法", max_length=10, null=False)
    header = models.TextField("请求头", null=True, default="{}")
    params_type = models.CharField("参数类型", max_length=10, null=False)
    params_body = models.TextField("参数内容", null=True, default="{}")
    result = models.TextField("结果", null=True, default="{}")
    assert_type = models.CharField("断言类型", max_length=10, null=True)
    assert_text = models.TextField("断言结果", null=True, default="{}")
    is_delete = models.BooleanField("删除状态", null=True, default=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    @property
    def project_id(self):
        return self.module.project_id

    def __str__(self):
        return self.name
