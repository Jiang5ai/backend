from rest_framework import serializers
from app_api.models.module_models import Module
from app_api.serializer.project import ProjectSerializer


class ModuleSerializer(serializers.ModelSerializer):
    """Module序列化"""
    # module_ForeignKey_project = serializers.CharField(source="project.name")  # 反向获取项目的名称
    # project = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Module
        fields = ["name", "describe", "project"]
        # depth = 1


class ModuleValidator(serializers.Serializer):
    """
    Module验证器
    """
    id = serializers.IntegerField(required=False)
    project_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True, error_messages={"required": "name不能为空"})
    describe = serializers.CharField(required=False)

    def create(self, validated_data):
        """
        创建
        """
        project = Module.objects.create(**validated_data)
        return project

    def update(self, instance, validated_data):
        """
        更新
        instance：更新的对象--从数据库里查出来的
        validated_data: 更新的数据--从request获取
        """
        instance.project_id = validated_data.get("project_id")
        instance.name = validated_data.get("name")
        instance.describe = validated_data.get("describe")
        instance.status = validated_data.get("status")
        instance.save()
        return instance
