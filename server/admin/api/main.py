from core.handlers import BaseAPIView, TemplateHTTPView


class MainView(BaseAPIView):
    template_name = 'admin/main.html'

    async def get(self, request, user):
        return self.render_template(request=request)
