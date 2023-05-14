from bson import ObjectId

from core.db import mongo
from core.handlers import BaseAPIView


class TariffsView(BaseAPIView):
    template_name = 'admin/tariffs.html'

    async def get(self, request, user):
        context = dict()
        filter_obj = {
            'status': 0
        }
        data = []
        async for tariff in mongo.tariffs.find(filter_obj).sort('_id', -1):
            if tariff.get('role_id') and ObjectId.is_valid(tariff['role_id']):
                tariff['role_id'] = await mongo.roles.find_one({'_id': ObjectId(tariff['role_id'])})
            else:
                tariff['role_id'] = {}
            data.append(tariff)

        context['roles'] = await mongo.roles.find({'status': 0}).to_list(length=None)
        context['data'] = data

        # CURRENT USER
        context['user'] = await mongo.users.find_one({'_id': ObjectId(user.id)})

        return self.render_template(request=request, **context)


class BrandsView(BaseAPIView):
    template_name = 'admin/brands.html'

    async def get(self, request, user):
        context = dict()

        filter_obj = {
            'status': 0
        }
        data = []
        async for brand in mongo.brands.find(filter_obj):
            data.append(brand)

        context['data'] = data

        # CURRENT USER
        context['user'] = await mongo.users.find_one({'_id': ObjectId(user.id)})

        return self.render_template(request=request, **context)


class SizesView(BaseAPIView):
    template_name = 'admin/sizes.html'

    async def get(self, request, user):
        context = dict()

        filter_obj = {
            'status': 0
        }
        data = []
        async for size in mongo.sizes.find(filter_obj):
            data.append(size)

        context['data'] = data

        # CURRENT USER
        context['user'] = await mongo.users.find_one({'_id': ObjectId(user.id)})

        return self.render_template(request=request, **context)


class ColorsView(BaseAPIView):
    template_name = 'admin/colors.html'

    async def get(self, request, user):
        context = dict()

        filter_obj = {
            'status': 0
        }
        data = []
        async for color in mongo.colors.find(filter_obj):
            data.append(color)

        context['data'] = data

        # CURRENT USER
        context['user'] = await mongo.users.find_one({'_id': ObjectId(user.id)})

        return self.render_template(request=request, **context)


class OverheadView(BaseAPIView):
    template_name = 'admin/overhead.html'

    async def get(self, request, user):
        context = dict()

        filter_obj = {
            'status': 0
        }
        data = {}
        overheads = await mongo.overheads.find(filter_obj).to_list(length=None)
        for x in overheads:
            data[str(x['_id'])] = x

        goods = await mongo.goods.aggregate([
            {'$match': {'status': 0}},
            {'$group': {'_id': '$overhead_id', 'count': {'$sum': '$count'},
                        'summa': {'$sum': {'$multiply': ['$count', '$purchase_price']}}}}
        ]).to_list(length=None)

        for x in goods:
            if data.get(x['_id']):
                data[x['_id']].update(x)

        context['data'] = [v for k, v in data.items()]

        # CURRENT USER
        context['user'] = await mongo.users.find_one({'_id': ObjectId(user.id)})

        return self.render_template(request=request, **context)
