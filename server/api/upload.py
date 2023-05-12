import os
import uuid

import aiofiles
from sanic import response
from sanic.views import HTTPMethodView

from settings import settings


class UploadView(HTTPMethodView):
    async def get(self, request):
        return response.json({
            '_success': True
        })

    async def post(self, request):
        file_path = settings.get('file_path', '') + '/static/uploads'
        file = request.files and request.files['file']
        file_name = ''

        if file:
            file = file[0]
            hashik = str(uuid.uuid4())
            ext = file.name.split('.')[len(file.name.split('.')) - 1]  # [::-1][0]
            file_name = f'{file_path}/{hashik[:2]}/{hashik[2:4]}/{hashik}.{ext}'
            os.makedirs(f'{file_path}/{hashik[:2]}/{hashik[2:4]}', 0o755, True)
            async with aiofiles.open(file_name, 'wb') as f:
                await f.write(file.body)
            file_name = f'{hashik[:2]}/{hashik[2:4]}/{hashik}.{ext}'

        return response.json({"file name": file_name})
