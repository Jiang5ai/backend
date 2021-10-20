from rest_framework import serializers
from app_api.models import TestTask, TaskCaseRelevance, TestCase


class TaskSerializer(serializers.ModelSerializer):
    """
    TaskCase序列化
    """
    cases = serializers.SerializerMethodField()

    class Meta:
        model = TestTask
        fields = ['id', 'name', 'describe', 'status', 'cases']

    def get_cases(self, testtask_obj):
        """查询task关联的case id list"""
        tcr = TaskCaseRelevance.objects.filter(task=testtask_obj)
        case_list = []
        for i in tcr:
            case_list.append(i.case_id)
        return case_list


class TaskValidator(serializers.Serializer):
    """
    Task验证器
    name = serializers.CharField("名称", max_length=100, blank=False, default="")
    describe = serializers.TextField("描述", null=True, default="")
    status = serializers.IntegerField("状态", default=0)  # 未执行、执行中、执行完成、排队中
    cases = serializers.TextField("关联用例", default="")  # "[1,2,3,4]"
    """
    name = serializers.CharField(required=True, max_length=50, error_messages={
        'required': "请输入测试任务名称",
        'invalid': "请输入正确的测试任务名称",
        'max_length': "测试任务名称名称不超过50字~"})

    describe = serializers.CharField(required=False)
    status = serializers.BooleanField(required=False)
    cases = serializers.SerializerMethodField(read_only=True)
    cases_list = serializers.ListField(required=True,
                                       error_messages={'required': "请输入关联用例", "not_a_list": "请输入list格式的cases"},
                                       write_only=True)

    def get_cases(self, testtask_obj):
        """查询task关联的case id list"""
        tcr = TaskCaseRelevance.objects.filter(task=testtask_obj)
        case_list = []
        for i in tcr:
            case_list.append(i.case_id)
        return case_list

    def validate_cases_list(self, value):
        """验证cases是否为List以及case是否存在"""
        if len(value) != 0:
            for c in value:
                try:
                    TestCase.objects.get(pk=c, is_delete=False)
                except (TestCase.DoesNotExist, ValueError):
                    raise serializers.ValidationError("case不存在")
            return value
        else:
            raise serializers.ValidationError("cases不能为空list")

    def create(self, validated_data):
        """
        创建
        """
        name = validated_data.get('name')
        describe = validated_data.get('describe')
        status = validated_data.get('status')
        case_list = validated_data.get('cases_list1')
        task = TestTask.objects.create(name=name, describe=describe, status=status)
        for case in case_list:
            TaskCaseRelevance.objects.create(task=task, case_id=case)
        return task

    def update(self, instance, validated_data):
        """
        更新
        instance：更新的对象--从数据库里查出来的
        validated_data: 更新的数据--从request获取
        """
        instance.name = validated_data.get("name")
        instance.describe = validated_data.get("describe")
        instance.status = validated_data.get("status")
        instance.cases = validated_data.get("cases")
        instance.save()
        return instance
