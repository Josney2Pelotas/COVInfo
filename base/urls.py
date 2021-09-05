from django.urls import path
from base.views import *

urlpatterns = [
    path('/', MainView.as_view(), name='visao_geral_dados')
]