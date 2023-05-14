import re

from sanic import response

from core.db import mongo
from core.handlers import TemplateHTTPView, auth, BaseAPIView
from core.hasher import generate_password

email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
phone_regex = "^\\+?[1-9][0-9]{7,14}$"
password_regex = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"


class UserSerializer:
    def __init__(
        self,
        id: str,
        name: list
    ):
        self.id = id

        self.name = name


class LoginAdminView(TemplateHTTPView):
    template_name = 'auth/admin/login.html'

    async def get(self, request):
        auth.logout_user(request)
        return self.render_template(request=request)

    async def post(self, request):
        username = str(request.json.get('username', ''))
        password = str(request.json.get('password', ''))

        if not username and not password:
            return response.json({
                '_success': False,
                'message': 'Required param(s)'
            })

        user = await mongo.users.find_one({
            'username': username,
            'password': generate_password(password=password),
            'status': {
                '$gte': 0
            }
        })

        if not user:
            return response.json({
                '_success': False,
                'message': 'user not found'
            })

        if user.get('status') == -2:
            return response.json({
                '_success': False,
                'message': 'you do not have access'
            })

        if not user.get('scope') or not isinstance(user.get('scope'), list):
            return response.json({
                '_success': False,
                'message': 'you do not have permissions'
            })

        user = UserSerializer(id=str(user['_id']), name=user['scope'])

        if user:
            auth.login_user(request, user)

            return response.json({
                '_success': True,
                'url': '/api/'
            })

        else:
            return response.json({
                '_success': False
            })


class LogoutAdminView(BaseAPIView):
    async def get(self, request, user):
        auth.logout_user(request)
        return response.redirect('/api/')
