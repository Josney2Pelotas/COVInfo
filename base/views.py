from django.views.generic import TemplateView
from django.http import JsonResponse


class MainView(TemplateView):
    def get(self, request):
        return JsonResponse({'teste': 'OK'})