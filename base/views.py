from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.shortcuts import render
from base.models import *
from base.forms import *
from datetime import datetime, date, timedelta
import pymysql.cursors


connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='1234',
    database='covinfo',
    cursorclass=pymysql.cursors.DictCursor
)


def ultimo_dia(datetime_obj):
    mes = datetime_obj.replace(day=28) + timedelta(days=4)
    return mes - timedelta(days=mes.day)


def geraDatas(ano):
    if ano == datetime.now().year:
        qtd_meses = datetime.now().month
    else:
        qtd_meses = 13

    datas = []
    for mes in range(1, qtd_meses):
        datas.append(ultimo_dia(date(ano, mes, 1)).strftime('%Y-%m-%d'))
    datas.append((datetime.now() - timedelta(1)).strftime('%Y-%m-%d'))
    return datas


def queryCasos(datas):
    with connection.cursor() as cursor:
        datas = "', '".join(datas)
        query = '''
                SELECT
                    sum(casos) as casos,
                    data
                FROM base_casos
                WHERE data IN ('{}')
                GROUP BY data;
                '''.format(datas)
        cursor.execute(query)
        dados_covid = cursor.fetchall()
    return dados_covid


class MainView(TemplateView):
    template = 'base/menu.html'
    def get(self, request):
        datas_filtro = geraDatas(2021)
        casos_total = queryCasos(datas_filtro)
        context = {
            'casos': casos_total,
            'ultima_atualizacao': Casos.objects.values_list('data').latest('data')[0].strftime('%d/%m/%Y'),
            'form': {
                'regiao': [('Todos', 'Todos')] + list(Regiao.objects.values_list('id', 'nome').order_by('nome').all()),
                'estado': [('Todos', 'Todos')] + list(Estado.objects.values_list('id', 'nome').order_by('nome').all()),
                'municipio': [('Todos', 'Todos')] + list(Municipio.objects.values_list('id', 'nome').order_by('nome').all())
            } 
        }
        return render(self.request, self.template, context)


def filtros(request):
    dados = request.POST.dict()
    del dados['csrfmiddlewaretoken']

    if dados['tipo'] == 'regiao':
        del dados['tipo']
        dados_municipio = {'estado__regiao': dados['regiao']}
        if dados['regiao'] == 'Todos':
            del dados['regiao']
        if dados_municipio['estado__regiao'] == 'Todos':
            del dados_municipio['estado__regiao']
        form = {
            'estado': [('Todos', 'Todos')] + list(Estado.objects.values_list('id', 'nome').order_by('nome').filter(**dados).all()),
            'municipio': [('Todos', 'Todos')] + list(Municipio.objects.values_list('id', 'nome').order_by('nome').filter(**dados_municipio).all())
        }
        template = 'base/filtros/filtro_regiao.html'

    if dados['tipo'] == 'estado':
        del dados['tipo']
        if dados['regiao'] == 'Todos':
            del dados['regiao']
        if dados['estado'] == 'Todos':
            del dados['estado']
        form = {
            'municipio': [('Todos', 'Todos')] + list(Municipio.objects.values_list('id', 'nome').order_by('nome').filter(**dados).all())
        }
        template = 'base/filtros/filtro_estado.html'

    retorno_filtros = render_to_string(template, {'form': form})
    return retorno_filtros
