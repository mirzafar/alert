from sanic import Blueprint

from .api.clients.auth import RegisterAPIView, LoginAPIView, LogoutAPIView
from .api.shop.profile import ProfileView
from .authentication import LoginAdminView
from .authentication import LogoutAdminView
from admin.api.cart.story import StoryView

admin_bp = Blueprint('admin')

admin_bp.add_route(LoginAdminView.as_view(), '/login/', name='login')
admin_bp.add_route(LogoutAdminView.as_view(), '/logout/', name='logout')

admin = Blueprint.group(
    admin_bp,
    url_prefix='/admin'
)

index_bp = Blueprint('index')

index_bp.add_route(StoryView.as_view(), '/', name='story')
index_bp.add_route(ProfileView.as_view(), '/profile/', name='shop.profile')

index_bp.add_route(LoginAPIView.as_view(), '/login/', name='shop.login')
index_bp.add_route(LogoutAPIView.as_view(), '/logout/', name='shop.logout')
index_bp.add_route(RegisterAPIView.as_view(), '/register/', name='shop.register')

index = Blueprint.group(
    index_bp,
    url_prefix='/'
)
