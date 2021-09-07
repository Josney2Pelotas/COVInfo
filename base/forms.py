from django import forms
from django.forms import widgets
from base.models import *


class LocalidadeForm(forms.Form):
    regiao = forms.ChoiceField(choices=[('Todos', 'Todos')] + list(Regiao.objects.values_list('id', 'nome').all()), label='Região', widget=forms.Select(attrs={'class':'row form-local input-field'}))
    estado = forms.ChoiceField(choices=[('Todos', 'Todos')] + list(Estado.objects.values_list('id', 'nome').all()), label='Estado', widget=forms.Select(attrs={'class':'row form-local'}))
    municipio = forms.ChoiceField(choices=[('Todos', 'Todos')] + list(Municipio.objects.values_list('id', 'nome').all()), label='Município', widget=forms.Select(attrs={'class':'row form-local'}))
