import asyncio
import os

from sanic import Sanic
from sanic_session import InMemorySessionInterface, Session

from core.auth import auth
from core.db import mongo
from settings import settings

app = Sanic(name='test')

app.config.AUTH_LOGIN_ENDPOINT = 'admin.login'

Session(app, interface=InMemorySessionInterface())


@app.listener('before_server_start')
async def initialize_modules(_app, _loop):
    mongo.initialize(_loop)
    auth.setup(_app)


# URLS SETUP
from admin import admin, index
from admin.api import api_group
from api.collection import CollectionView
from api.upload import UploadView

app.blueprint([
    index,
    admin,
    api_group
])

app.add_route(CollectionView.as_view(), '/collection/<collection_name>/<action>/', name='collection.action')
app.add_route(UploadView.as_view(), '/upload/', name='upload')

app.static('/static', os.path.join(settings.get('file_path'), 'static'))

if __name__ == '__main__':
    try:
        app.run('0.0.0.0', port=7019, access_log=False, auto_reload=False, debug=True)
    except Exception as e:
        print(e)
        loop = asyncio.get_event_loop()
