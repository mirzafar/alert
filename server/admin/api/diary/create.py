from core.db import mongo
from core.handlers import BaseAPIView


class DiaryCreateView(BaseAPIView):
    template_name = 'admin/diary-create.html'

    async def get(self, request, user):
        users = await mongo.users.find({'status': 0}).to_list(length=None)
        return self.render_template(request=request, users=users)
