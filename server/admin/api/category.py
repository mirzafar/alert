from core.db import mongo
from core.handlers import TemplateHTTPView, BaseAPIView


class CategoryView(BaseAPIView):
    template_name = 'admin/category.html'

    async def get(self, request, user):
        filter_obj = {
            'status': 0
        }
        data = await mongo.category.find(filter_obj).sort('created_at', -1).to_list(length=None)
        return self.render_template(request=request, data=data)
