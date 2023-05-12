from core.db import mongo
from core.handlers import BaseAPIView


class ApplicationsView(BaseAPIView):
    template_name = 'admin/applications.html'

    async def get(self, request, user):
        data = await mongo.applications.find({'status': 0}).sort('_id', -1).to_list(length=None)
        return self.render_template(request=request, data=data)

    async def post(self, request, user):
        pass
