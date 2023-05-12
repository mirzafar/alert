from core.db import mongo
from core.handlers import BaseAPIView


class ExpensesView(BaseAPIView):
    template_name = 'admin/analytics/expenses.html'

    async def get(self, request, user):
        context = dict()

        filter_obj = {
            'status': 0,
        }
        data = []
        async for expense in mongo.expenses.find(filter_obj).sort('_id', -1):
            data.append(expense)

        context['data'] = data
        return self.render_template(request=request, **context)
