from django.urls import path
from base.views import *

urlpatterns = [
    path('', MainView.as_view(), name='visao_geral_dados'),
    path('filtros/', filtros, name='filtro_dos_filtros')
]
