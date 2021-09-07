from django.views.generic import TemplateView
from django.shortcuts import render
from base.models import *
from base.forms import *


class MainView(TemplateView):
    template = 'base/menu.html'
    def get(self, request):
        context = {
            'ultima_atualizacao': Casos.objects.values_list('data').latest('data')[0].strftime('%d/%m/%Y'),
            'form': {
                'regiao': [('Todos', 'Todos')] + list(Regiao.objects.values_list('id', 'nome').order_by('nome').all()),
                'estado': [('Todos', 'Todos')] + list(Estado.objects.values_list('id', 'nome').order_by('nome').all()),
                'municipio': [('Todos', 'Todos')] + list(Municipio.objects.values_list('id', 'nome').order_by('nome').all())
            } 
        }
        return render(self.request, self.template, context)
