from collections import namedtuple
from functools import partial, wraps
from inspect import isawaitable

from sanic import response

__all__ = ['auth']

from settings import settings

User = namedtuple('User', 'id name'.split())


class Auth:

    def __init__(self, app=None):
        self.app = None
        if app is not None:
            self.setup(app)

    def setup(self, app):
        if self.app is not None:
            raise RuntimeError('already initialized with an application')
        self.app = app
        get = app.config.get
        self.login_endpoint = get('AUTH_LOGIN_ENDPOINT', 'auth.login')
        self.login_url = get('AUTH_LOGIN_URL', None)
        session = get('AUTH_SESSION_NAME', get('SESSION_NAME', 'session'))
        self.session_name = session
        self.auth_session_key = get('AUTH_TOKEN_NAME', '_auth')

    def login_user(self, request, user):
        self.get_session(request)[self.auth_session_key] = self.serialize(user)

    def logout_user(self, request):
        return self.get_session(request).pop(self.auth_session_key, None)

    def current_user(self, request):
        token = self.get_session(request).get(self.auth_session_key, None)
        if token is not None:
            return self.load_user(token)

    def login_required(self, route=None, *, user_keyword=None,
                       handle_no_auth=None, name=None, return_url=None):
        if route is None:
            return partial(self.login_required, user_keyword=user_keyword,
                           handle_no_auth=handle_no_auth, name=name, return_url=return_url)
        if handle_no_auth is not None:
            assert callable(handle_no_auth), 'handle_no_auth must be callable'

        @wraps(route)
        async def privileged(request, *args, **kwargs):
            user = self.current_user(request)
            if isawaitable(user):
                user = await user

            if user is None or name is None or not list(set(user.name) & set(name)):
                if handle_no_auth:
                    resp = handle_no_auth(request)
                else:
                    resp = self.handle_no_auth(request, return_url)
            else:
                if user_keyword is not None:
                    if user_keyword in kwargs:
                        raise RuntimeError(
                            'override user keyword %r in route' % user_keyword)
                    kwargs[user_keyword] = user
                resp = route(request, *args, **kwargs)

            if isawaitable(resp):
                resp = await resp
            return resp

        return privileged

    def serialize(self, user):
        return {'uid': user.id, 'name': user.name}

    def serializer(self, user_serializer):
        self.serialize = user_serializer
        return user_serializer

    def load_user(self, token):
        if token is not None:
            return User(id=token['uid'], name=token['name'])

    def user_loader(self, load_user):
        self.load_user = load_user
        return load_user

    def get_session(self, request):
        return request.ctx.session

    def handle_no_auth(self, request, return_url=None):
        u = return_url or self.login_url or request.app.url_for(self.login_endpoint)
        return response.redirect(u)

    def no_auth_handler(self, handle_no_auth):
        self.handle_no_auth = handle_no_auth
        return handle_no_auth


auth = Auth()
