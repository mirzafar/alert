import re

from bson import ObjectId

from core.db import mongo
from core.handlers import BaseAPIView

email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class UsersCreateView(BaseAPIView):
    template_name = 'admin/users-create.html'

    async def get(self, request, user):
        context = dict()

        context['roles'] = await mongo.roles.find({'status': 0}).to_list(length=None)

        # CURRENT USER
        context['user'] = await mongo.users.find_one({'_id': ObjectId(user.id)})

        return self.render_template(request=request, **context)
