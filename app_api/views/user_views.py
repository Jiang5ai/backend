from django.contrib.auth.models import User, Group
from django.contrib import auth
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from app_common.utils.response import response, Error
import json


# Create your views here.

class LoginView(APIView):
    #  这个接口的调用不能加认证
    authentication_classes = []

    def post(self, request):
        """
        登录账号，并获取token
        """
        login_username = request.data.get("username", "")
        login_password = request.data.get("password", "")
        if login_username == '' or login_password == '':
            return response(error=Error.USER_OR_PAWD_NULL)
        else:
            user = auth.authenticate(username=login_username, password=login_password)

            if user is not None and user.is_active:
                auth.login(request, user)  # 验证登录
                # update the token
                token = Token.objects.filter(user=user)
                token.delete()
                token = Token.objects.create(user=user)
                user_info = {
                    "id": user.id,
                    "name": login_username
                }
                user_str = json.dumps(user_info)
                print(user_str)
                return response(data={"Token": str(token), "User": user_str})
            else:
                return response(error=Error.USER_OR_PAWD_ERROR)

    def delete(self, request):
        """
        退出账号，并删除token
        """
        userId = request.data.get("id")
        token = Token.objects.filter(user=userId)
        token.delete()
        return response()
