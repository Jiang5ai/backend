from rest_framework import serializers
from app_api.models import TestCase


class CaseData:
    methods = ["POST", "GET", "PUT", "DELETE"]
    params_type = ["params", "form", "json"]
    assert_type = ["include", "equal"]


class CaseSerializer(serializers.ModelSerializer):
    """Case序列化"""
    module_ForeignKey_project = serializers.CharField(source="project.name")  # 反向获取项目的名称

    # project = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = TestCase
        fields = ["name", "describe", "module_ForeignKey_project"]
        # depth = 1


class CaseValidator(serializers.Serializer):
    """
    Case验证器
    """
    module_id = serializers.IntegerField(required=True)

    name = serializers.CharField(required=True, max_length=100, error_messages={
        'required': "请输入项目名称~",
        'max_length': "项目名称不超过250字~"})

    url = serializers.CharField(required=True, error_messages={'required': "URL不能为空~"})

    method = serializers.ChoiceField(required=True, choices=CaseData.methods, error_messages={
        "required": "请求方法不能为空~",
        "invalid_choice": "只支持POST/GET/PUT/DELETE"})

    header = serializers.JSONField(required=False)

    params_type = serializers.ChoiceField(required=False, choices=CaseData.params_type,
                                          error_messages={"invalid_choice": "只支持params\\form\\json类型"})

    params_body = serializers.CharField(required=False)

    result = serializers.CharField(required=True, error_messages={'required': "result不能为空~"})

    assert_type = serializers.ChoiceField(required=False, choices=CaseData.assert_type,
                                          error_messages={"invalid_choice": "只支持include\\equal类型"})

    assert_text = serializers.CharField(required=True, error_messages={'required': "assert_text不能为空~"})

    def create(self, validated_data):
        """
        创建
        """
        project = TestCase.objects.create(**validated_data)
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
