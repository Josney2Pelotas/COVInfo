from django.urls import path
from base.views import *

urlpatterns = [
    path('teste/', TesteView.as_view(), name='teste')
]