from core.db import mongo
from core.handlers import BaseAPIView


class GoodCreateView(BaseAPIView):
    template_name = 'admin/good-create.html'

    async def get(self, request, user):
        context = dict()
        context['category'] = await mongo.category.find({'status': 0}).to_list(length=None)
        context['sizes'] = await mongo.sizes.find({'status': 0}).to_list(length=None)
        context['colors'] = await mongo.colors.find({'status': 0}).to_list(length=None)
        context['brands'] = await mongo.brands.find({'status': 0}).to_list(length=None)
        context['overheads'] = await mongo.overheads.find({'status': 0}).to_list(length=None)
        return self.render_template(request=request, **context)
