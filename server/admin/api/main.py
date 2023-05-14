from bson import ObjectId

from core.db import mongo
from core.handlers import BaseAPIView, TemplateHTTPView


class MainView(BaseAPIView):
    template_name = 'admin/main.html'

    async def get(self, request, user):
        # CURRENT USER
        user = await mongo.users.find_one({'_id': ObjectId(user.id)})

        return self.render_template(
            request=request,
            user=user
        )
