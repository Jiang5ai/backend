from rest_framework import serializers
from app_api.models import Project


# class ProjectSerializer(serializers.ModelSerializer):
#     """Project序列化"""
#
#     class Meta:
#         model = Project
#         fields = ["id", "name", "describe", "status"]
#
#
# class ProjectValidator(serializers.Serializer):
#     """
#     Project验证器
#     """
#     id = serializers.IntegerField(required=False)
#     name = serializers.CharField(required=True, error_messages={"required": "name不能为空"})
#     describe = serializers.CharField(required=False)
#     status = serializers.BooleanField(required=False)
#
#     def create(self, validated_data):
#         """
#         创建
#         """
#         project = Project.objects.create(**validated_data)
#         return project
#
#     def update(self, instance, validated_data):
#         """
#         更新
#         instance：更新的对象--从数据库里查出来的
#         validated_data: 更新的数据--从request获取
#         """
#         instance.name = validated_data.get("name")
#         instance.describe = validated_data.get("describe")
#         instance.status = validated_data.get("status")
#         instance.save()
#         return instance

class ProjectSerializer(serializers.ModelSerializer):
    """
    默认是这样的
    id = IntegerField(label='ID', read_only=True)
    name = CharField(label='名称', max_length=100)
    describe = CharField(allow_null=True, label='描述', max_length=250, required=False)
    status = BooleanField(allow_null=True, label='状态', required=False)
    """
    # 反序列化
    name = serializers.CharField(max_length=100, error_messages={
        'required': "请输入项目名称~",
        'max_length': "项目名称不超过250字~"

    })
    describe = serializers.CharField(required=False, max_length=250, error_messages={
        'max_length': "描述不超过250字~"
    })

    class Meta:
        model = Project
        fields = ["id", "name", "describe", "status"]
