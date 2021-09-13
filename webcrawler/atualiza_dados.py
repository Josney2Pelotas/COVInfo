import requests, json, os, datetime , pymysql.cursors, pandas as pd

connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='1234',
    database='covinfo',
    cursorclass=pymysql.cursors.DictCursor
)


def download_planilha():
    url = 'https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalGeralApi'
    request_endpoint = requests.get(url)
    endpoint_json = json.loads(request_endpoint.text)
    request_planilha = requests.get(endpoint_json['planilha']['arquivo']['url'])
    path_xlsx = os.path.dirname(os.path.realpath(__file__)) + '\\info_diaria.xlsx'
    output = open(path_xlsx, 'wb')
    output.write(request_planilha.content)
    output.close()


def atualiza_dados():
    planilha = os.path.dirname(os.path.realpath(__file__)) + '\\info_diaria.xlsx'
    dia_anterior = (datetime.date.today()-datetime.timedelta(1)).strftime("%Y-%m-%d")
    dados_planilhas = pd.read_excel(planilha)
    dados_planilhas.dropna(subset = ["municipio"], inplace=True)
    dados_planilhas['Recuperadosnovos'] = dados_planilhas['Recuperadosnovos'].fillna(0)
    dados_planilhas['emAcompanhamentoNovos'] = dados_planilhas['emAcompanhamentoNovos'].fillna(0)
    total_linhas = len(dados_planilhas.index)
    contador = 1

    with connection.cursor() as cursor:
        for linha in dados_planilhas.iterrows():
            query_dados_regiao = '''
                                 SELECT
                                    regiao.id AS regiao_id,
                                    estado.id AS estado_id,
                                    municipio.id AS municipio_id
                                 FROM base_regiao AS regiao
                                    INNER JOIN base_estado AS estado
                                        ON estado.regiao_id = regiao.id
                                    INNER JOIN base_municipio AS municipio
                                        ON municipio.estado_id = estado.id
                                 WHERE regiao.nome = %s AND estado.sigla = %s AND municipio.nome = %s
                                 '''
            cursor.execute(query_dados_regiao, [linha[1]['regiao'], linha[1]['estado'], linha[1]['municipio']])
            dados_municipio = cursor.fetchall()

            query_dia_anterior = 'SELECT casos, obitos FROM base_casos WHERE data = %s AND municipio_id = %s'
            cursor.execute(query_dia_anterior, [dia_anterior, dados_municipio[0]['municipio_id']])
            dados_dia_anterior = cursor.fetchall()

            casosNovos = dados_dia_anterior[0]['casos'] - linha[1]['casosAcumulado']
            obitosNovos = dados_dia_anterior[0]['obitos'] - linha[1]['obitosAcumulado']

            query_insert =  '''
                            INSERT INTO base_casos(casos, casos_novos, obitos, obitos_novos, recuperados, acompanhamento, semana, data, regiao_id, estado_id, municipio_id) VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            '''
            cursor.execute(query_insert, [
                linha[1]['casosAcumulado'],
                casosNovos,
                linha[1]['obitosAcumulado'],
                obitosNovos,
                linha[1]['Recuperadosnovos'],
                linha[1]['emAcompanhamentoNovos'],
                linha[1]['semanaEpi'],
                linha[1]['data'],
                dados_municipio[0]['regiao_id'],
                dados_municipio[0]['estado_id'],
                dados_municipio[0]['municipio_id']
            ])
            connection.commit()

            print('Linha ' + str(contador) + ' de ' + str(total_linhas) + ' Inserida')
            contador += 1
        cursor.close()
    return 0


print('-----------------------------Iniciando Coleta da Planilha Diária-----------------------------')
download_planilha()
print('---------------------------------------Planilha Gerada---------------------------------------')

print('-------------------------------Iniciando Insert dos Dados Novos------------------------------')
atualiza_dados()
print('---------------------------------Dados Atualizados com Sucesso-------------------------------')
