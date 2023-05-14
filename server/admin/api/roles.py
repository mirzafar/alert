from bson import ObjectId

from core.db import mongo
from core.handlers import BaseAPIView


class RolesView(BaseAPIView):
    template_name = 'admin/roles.html'

    async def get(self, request, user):
        filter_obj = {
            'status': 0
        }
        data = await mongo.roles.find(filter_obj).sort('created_at', -1).to_list(length=None)
        user = await mongo.users.find_one({'_id': ObjectId(user.id)})

        return self.render_template(
            request=request,
            data=data,
            user=user
        )
