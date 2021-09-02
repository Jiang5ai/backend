from django.db import models


# Create your models here.

class Project(models.Model):
    """
    项目表
    """
    name = models.CharField("名称", max_length=100, null=False)
    describe = models.CharField("描述", max_length=250, null=True, default="")
    status = models.BooleanField("状态", null=True, default=True)
    is_delete = models.BooleanField("删除状态", null=True, default=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return self.name
