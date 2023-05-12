from sanic import Blueprint

from .applications import ApplicationsView
from .cart import story_bp
from .category import CategoryView
from .diary import diary_bp
from .employees import employees_bp
from .analytics import analytics_bp
from .pre_orders import pre_orders_bp
from .tools import tools_bp
from .goods import goods_bp
from .info import InfoView
from .main import MainView
from .orders import receipts_bp
from .roles import RolesView
from .users import UsersView, users_bp
from .aboutUs import AboutUsView
from .contact import ContactView
from .views import TariffsView, BrandsView, SizesView, ColorsView, OverheadView

api = Blueprint('api')

api.add_route(RolesView.as_view(), '/roles/', name='roles')
api.add_route(TariffsView.as_view(), '/tariffs/', name='tariffs')
api.add_route(BrandsView.as_view(), '/brands/', name='brands')
api.add_route(OverheadView.as_view(), '/overheads/', name='overheads')
api.add_route(SizesView.as_view(), '/sizes/', name='sizes')
api.add_route(ColorsView.as_view(), '/colors/', name='colors')
api.add_route(CategoryView.as_view(), '/category/', name='category')
api.add_route(ApplicationsView.as_view(), '/applications/', name='applications')
api.add_route(InfoView.as_view(), '/info/', name='info')
api.add_route(ContactView.as_view(), '/contact/', name='contact')
api.add_route(AboutUsView.as_view(), '/about/', name='about')
api.add_route(MainView.as_view(), '', name='main')

api_group = Blueprint.group(
    api,
    goods_bp,
    diary_bp,
    analytics_bp,
    receipts_bp,
    pre_orders_bp,
    users_bp,
    employees_bp,
    story_bp,
    tools_bp,
    url_prefix='/api'
)
