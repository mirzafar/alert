import string
import sys

from bson import ObjectId
from pydantic import ValidationError
from sanic import response
from sanic.views import HTTPMethodView

from core.db import mongo
from .models import *


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


class CollectionView(HTTPMethodView):
    async def get(self, request):
        return response.json({
            '_success': True
        })

    async def post(self, request, collection_name, action):
        payload = request.json
        if not payload:
            return response.json({
                '_success': False,
                'message': 'Missing options'
            })
        if action == 'add':
            refuse_fields = ['_id', 'status', 'undefined']
            item = {k: v for k, v in payload.items() if k not in refuse_fields}
            item['status'] = 0
            item['created_at'] = datetime.now()

            try:
                print(item)
                item = str_to_class(string.capwords(collection_name, sep=None))(**{k: v for k, v in item.items() if k})
                print(item.dict())
                await mongo[collection_name].insert_one(item.dict())
            except ValidationError as er:
                er = er.errors()
                err = [f'{[i for i in x.get("loc")]}: {x.get("msg")}' for x in er]
                return response.json({
                    '_success': False,
                    'message': ', '.join(err)
                })

            return response.json({
                '_success': True,
                'message': 'Added successfully'
            })

        else:
            _id = ObjectId(action)
            if not ObjectId.is_valid(_id):
                return response.json({
                    '_success': False,
                    'message': 'Invalid param(s): id'
                })

            if payload.get('status') == -1:
                await mongo[collection_name].update_one({'_id': _id},
                                                        {'$set': {'status': -1, 'deleted_at': datetime.now()}})
                return response.json({
                    '_success': True,
                    'message': 'Deleted successfully'
                })

            if payload.get('undefined'):
                del payload['undefined']
            if payload.get('_id'):
                del payload['_id']

            try:
                payload['updated_at'] = datetime.now()
                payload = str_to_class(string.capwords(collection_name, sep=None))(**payload)
                await mongo[collection_name].update_one({'_id': _id}, {'$set': payload.dict(exclude_none=True)})
            except ValidationError as er:
                er = er.errors()
                err = [f'{[i for i in x.get("loc")]}: {x.get("msg")}' for x in er]
                return response.json({
                    '_success': False,
                    'message': ', '.join(err)
                })

        return response.json({
            '_success': True
        })
