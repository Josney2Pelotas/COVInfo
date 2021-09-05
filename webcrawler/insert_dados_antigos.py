import os, pymysql.cursors, pandas as pd

connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='1234',
    database='covinfo',
    cursorclass=pymysql.cursors.DictCursor
)


def dados_antigos():
    #Trocar nome_planilha.csv para o nome do csv usado
    planilha = os.path.dirname(os.path.realpath(__file__)) + '\\nome_planilha.csv'
    df = pd.read_csv(planilha, sep=';')
    df.dropna(subset = ["municipio"], inplace=True)
    df['Recuperadosnovos'] = df['Recuperadosnovos'].fillna(0)
    df['emAcompanhamentoNovos'] = df['emAcompanhamentoNovos'].fillna(0)
    for row in df.iterrows():
        with connection.cursor() as cursor:
            query = '''
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
            cursor.execute(query, [row[1]['regiao'], row[1]['estado'], row[1]['municipio']])
            resultado = cursor.fetchall()
            query_insert =  '''
                            INSERT INTO base_casos(casos, casos_novos, obitos, obitos_novos, recuperados, acompanhamento, semana, data, regiao_id, estado_id, municipio_id) VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            '''
            cursor.execute(query_insert, [
                row[1]['casosAcumulado'],
                row[1]['casosNovos'],
                row[1]['obitosAcumulado'],
                row[1]['obitosNovos'],
                row[1]['Recuperadosnovos'],
                row[1]['emAcompanhamentoNovos'],
                row[1]['semanaEpi'],
                row[1]['data'],
                resultado[0]['regiao_id'],
                resultado[0]['estado_id'],
                resultado[0]['municipio_id']
            ])
            connection.commit()
            cursor.close()
    return '-----------------------------Fim da Inserção de Casos-----------------------------'


print('-----------------------------Iniciando Inserção de Casos Antigos-----------------------------')
dados_antigos()
