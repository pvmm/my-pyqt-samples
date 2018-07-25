﻿# -*- coding: UTF-8 -*-
from json import loads, dumps
import re, string, sys, os
import urllib.request
import urllib.parse
from difflib import SequenceMatcher
from operator import itemgetter
from unicodedata import normalize
import encodings.idna

# Envia mensagem de log para saída padrão.
if 'DEBUG' in os.environ:
    from logger import StdoutLogger as Logger
else:
    from kivy.logger import Logger

def gera_lista_final(dct_pesquisa):
    '''
    Recebe dicionário com dados do arquivo csv (lista de dicionários com a chave e com as colunas a serem geocodificadas) e lista de colunas na ordem que deve ser feita a geocodificação.
    Monta a lista final que será gravada em novo arquivo csv aplicando a função _consulta_geocode para cada registro.
    '''
    try:
        dados = dct_pesquisa['dados']
        colunas = dct_pesquisa['prioridade']
        geocode_service = dct_pesquisa['geocode_service']

        dados_finais = []
        total = len(dados)
        ct = 1

        for d in dados:

            lb_key = 'KEY'
            key = d[lb_key]

            dct = {lb_key: key}

            for c in colunas:
                if c in list(d.keys()):
                    result_set = _consulta_geocode(d[c], c, geocode_service)
                    dct.update(result_set)
                    if dct['SIMILARIDADE']!=0.0:
                        break

            dados_finais.append(dct)

            Logger.debug('prep_geocode: {0} de {1}'.format(ct, total))
            ct += 1

        return dados_finais
    except Exception as e:
        Logger.error('prep_code: Erro ao gerar lista final: %s' % e)


def _consulta_geocode(string_pesquisa, coluna, geocode_service):
    '''
    Recebe a string a ser geocodificada e sua coluna correspondente.
    Consulta a API de geocodificação e avalia o resultado, retornando o dicionário que será inserido na lista final.
    '''
    try:
        dct = {}
        encontrou = False

        str_pesquisa = _remove_acentos(string_pesquisa)
        dado_reduzido = _reduz_dado(str_pesquisa)

        for d in dado_reduzido[::-1]:
            str_json = _consulta_api(d, geocode_service)
            resultado_consulta = _avalia_resultado(d, str_json)

            if resultado_consulta:
                dct.update({'COLUNA_PESQ': coluna, 'DADO_COMPL_PESQ': dado_reduzido[-1], 'DADO_PESQ': d})
                dct.update(resultado_consulta)
                encontrou = True
                break

        if encontrou==False:
            dct.update({'COLUNA_PESQ': 'ALL', 'DADO_COMPL_PESQ': 'ALL', 'DADO_PESQ': 'ALL', 'LONG': 'NOT FOUND', 'LAT': 'NOT FOUND', 'LOCAL_ENCONTRADO': 'NOT FOUND', 'SIMILARIDADE': 0.0})
        return dct

    except Exception as e:
        Logger.error('prep_geocode: Erro ao montar novo registro: %s' % e)



def _reduz_dado(dado):
    '''
    Recebe uma string e retorna uma lista com todas as possibilidades de pesquisa (string inteira e suas reduções de até 2 palavras). Ex: 'QD 400 LT B APT 201' => ['QD 400','QD 400 LT','QD 400 LT B','QD 400 LT B APT','QD 400 LT B APT 201']
    '''
    s = dado.replace('.', '').replace(',', ' ').split()
    if len(s) >= 2:
        base = s[0] + ' ' + s[1]
        dados = [base]
        for x in range(2,len(s)):
            base += ' ' + s[x]
            dados.append( base )
        return dados
    else:
        return s


def _consulta_api(local, geocode_service):
    '''
    Recebe a descrição de um local e faz a pesquisa do mesmo na API de geocodificação
    '''
    try:
        # consulta = 'http://geocode.codeplan.df.gov.br/?{0}'
        consulta = geocode_service + '/?{0}' if geocode_service[-1] != '/' else geocode_service + '?{0}'
        Logger.debug('prep_geocode: ' + consulta)
        parametros = urllib.parse.urlencode({'localidade': local, 'limite': '33'})
        result = urllib.request.urlopen(consulta.format(parametros))
        result_set = result.read()
        str_json = result_set.decode('utf-8')
        return str_json
    except Exception as e:
        Logger.error('prep_geocode: Erro ao consultar API de geocodificação: %s' % e)


def testa_conexao(geocode_service):
    '''
    Recebe a descrição de um local e faz a pesquisa do mesmo na API de geocodificação
    '''
    try:
        consulta = geocode_service + '/?{0}' if geocode_service[-1] != '/' else geocode_service + '?{0}'
        parametros = urllib.parse.urlencode({'localidade': '', 'limite': '1'})
        result = urllib.request.urlopen(consulta.format(parametros))
        http_code = result.code
        return http_code
    except Exception as e:
        Logger.error('prep_geocode: Erro ao consultar API de geocodificação: %s' % e)


def _avalia_resultado(dado_busca, str_json):
    '''
    Recebe a string resultante da consulta à API e a string consultada.
    Retorna dicionário com local encontrado, similaridade e coordenadas (latitude e longitude)
    '''
    try:
        geojson = loads(str_json)
        features = geojson['features']

        if features:
            dados = []
            for f in features:
                # nome_local = f['properties']['nome'].encode('utf8')
                nome_local = f['properties']['nome']

                local = {
                    'LOCAL_ENCONTRADO': nome_local,
                    'COORDENADAS': f['geometry']['coordinates']
                }
                dados.append(local)


            for d in dados:
                # similaridade = round(SequenceMatcher(None, d['LOCAL_ENCONTRADO'].ljust(maior).upper(), dado_busca.upper()).ratio(), 5)
                similaridade = round(SequenceMatcher(None, d['LOCAL_ENCONTRADO'].upper(), dado_busca.upper()).ratio(), 5)
                d.update({'SIMILARIDADE': similaridade})

            dados_ordenados = sorted(dados, key=itemgetter('SIMILARIDADE'))
            melhor_resultado = dados_ordenados[-1]
            melhor_resultado.update({'LONG': melhor_resultado['COORDENADAS'][0], 'LAT': melhor_resultado['COORDENADAS'][1]})
            del melhor_resultado['COORDENADAS']

            return melhor_resultado
        else:
            resultado = {}
            return resultado

    except Exception as e:
        Logger.error('prep_geocode: Erro ao gerar lista final: %s' % e)


def _remove_acentos(txt):
    '''
    Recebe string e remove toda a acentuação gráfica
    Disponível em: https://wiki.python.org.br/RemovedorDeAcentos
    '''
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def fatia_lista(lista, n):
    '''
    Recebe uma lista e divide-a em n sublistas
    '''
    for i in range(0, len(lista), n):
        yield lista[i:i + n]
