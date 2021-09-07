from django.db import models


class Casos(models.Model):
    casos = models.FloatField()
    casos_novos = models.FloatField()
    obitos = models.FloatField()
    obitos_novos = models.FloatField()
    recuperados = models.FloatField()
    acompanhamento = models.FloatField()
    semana = models.IntegerField()
    data = models.DateField()
    regiao = models.ForeignKey('Regiao', models.DO_NOTHING)
    estado = models.ForeignKey('Estado', models.DO_NOTHING)
    municipio = models.ForeignKey('Municipio', models.DO_NOTHING)


class Estado(models.Model):
    nome = models.CharField(max_length=255)
    sigla = models.CharField(max_length=10)
    regiao = models.ForeignKey('Regiao', models.DO_NOTHING)


class Municipio(models.Model):
    nome = models.CharField(max_length=255)
    populacao = models.FloatField()
    estado = models.ForeignKey(Estado, models.DO_NOTHING)


class Regiao(models.Model):
    nome = models.CharField(max_length=255)
