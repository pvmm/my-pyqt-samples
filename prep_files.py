# -*- coding: UTF-8 -*-
import csv, uuid, os, zipfile, string, platform
from logger import StdoutLogger as Logger

label_key = 'KEY'

# Envia mensagem de log para saída padrão.
if 'DEBUG' in os.environ:
    from logger import StdoutLogger as Logger

def formata_nome_arquivo(nome_arquivo):
    '''
    Recebe o path do arquivo e retira no início a substring 'file://'
    '''
    # list_path = nome_arquivo.split(os.sep)
    # del list_path[0:3]
    # # print(os.sep.join(list_path))
    # # return os.path.join()
    # return ''
    return nome_arquivo.replace('file:%s%s' % (os.sep, os.sep), '')

def lista_colunas_e_dados(arquivo_original, delimitador):
    '''
    Abre arquivo csv original e adiciona uma chave única a cada registro. Retorna lista de registros (cada registro é um dicionário) e lista com elementos do cabeçalho do arquivo original.
    '''
    try:
        with open(arquivo_original, encoding='latin-1') as arquivo:
            dict_reader = csv.DictReader(arquivo, delimiter=str(delimitador))
            # dict_reader = csv.DictReader(arquivo, delimiter=str(delimitador), dialect='excel')
            headers_arquivo = dict_reader.fieldnames
            linhas = []
            for l in dict_reader:
                if None not in l.keys() and None not in l.values():
                    key = uuid.uuid4()
                    l[label_key] = str(key)
                    linhas.append(l)

        Logger.debug('prep_files: linhas = %i.' % len(linhas))
        return linhas, headers_arquivo

    except (IOError, TypeError, csv.Error) as e:
        Logger.error('prep_files: Erro ao manipular arquivo original: %s' % e)
        raise e
    except Exception as e:
        Logger.error('prep_files: Verifique o arquivo csv de entrada: %s' % e)
        raise e

def prepara_dados(dados, campos_selecionados):
    '''
    Recebe lista dos dados do arquivo original e as colunas a serem geocodificadas. Retorna lista de dicionários com a chave e com as colunas recebidas.
    '''
    try:
        dados_pesquisa = []
        for d in dados:
            dct = {}
            dct[label_key] = d[label_key]
            for c in campos_selecionados:
                if c in list(d.keys()):
                    dct[c] = d[c]
            dados_pesquisa.append(dct)
        return dados_pesquisa
    except Exception as e:
        Logger.error('prep_files: Erro ao preparar dados para geocodificação: %s' % e)

def padroniza_dados(dados):
    '''
    Recebe lista de dicionários com chave e colunas a serem geocodificadas, aplica a função 'troca_verbetes' para cada coluna e retorna nova lista.
    '''
    try:
        for d in dados:
            c = d.keys()
            chaves = list(c)
            chaves.remove(label_key)
            for k in chaves:
                valor = d[k]
                d[k] = _troca_verbetes(valor)
        return dados
    except Exception as e:
        Logger.error('prep_files: Erro ao padronizar dados para geocodificação: %s' % e)


def _troca_verbetes(dado):
    '''
    Recebe uma string e substitui verbetes comuns por sinônimos
    '''
    s = dado.split()
    for x in range(0, len(s)):
        if s[x].lower() in ['conjunto','conj','conj.','cj','cj.']:
            s[x] = 'CJ'
        elif s[x].lower() in ['lote','lt','lt.']:
            s[x] = 'LT'
        elif s[x].lower() in ['loja','lj','lj.']:
            s[x] = 'LJ'
        elif s[x].lower() in ['bloco','bl','bl.']:
            s[x] = 'BL'
        elif s[x].lower() in ['q.','qd','qd.','quadra']:
            s[x] = 'QD'
        elif s[x].lower() in ['apartamento','apto','apt','apt.','ap','ap.']:
            s[x] = 'APT'
        elif s[x].lower() in ['condomínio','condominio','cond','cond.']:
            s[x] = 'Cond'
        elif s[x].lower() in ['rua','r.']:
            s[x] = 'Rua'
        elif s[x].lower() in ['alameda','al','al.']:
            s[x] = 'Alameda'
        elif s[x].lower() in ['setor','set','set.','st','st.']:
            s[x] = 'Setor'
        elif s[x].isdigit():
            num_int = int(s[x])
            s[x] = str(num_int)
    return ' '.join(s)

def gera_arquivo(lista_final, prefixo, dir_arquivo, labels):
    '''
    Recebe lista final e lista de argumentos da execução (nome do arquivo original e colunas a serem manipuladas) e grava novo arquivo .csv
    '''
    try:
        diretorio_saida, arquivo = _identifica_diretorio(dir_arquivo)
        diretorio = os.path.join(diretorio_saida, 'files_%s' % arquivo.replace('.csv', ''))

        if not os.path.exists(diretorio):
            os.makedirs(diretorio)

        novo_arquivo = os.path.join(diretorio, '%s_%s' % (prefixo, arquivo))

        with open(novo_arquivo, 'w', encoding='latin-1') as saida:

            if label_key not in labels:
                labels.insert(0, label_key)

            dict_writer = csv.DictWriter(saida, fieldnames=labels, delimiter=';')
            # dict_writer = csv.DictWriter(saida, fieldnames=labels, delimiter=';', dialect='excel')
            dict_writer.writeheader()
            for l in lista_final:
                dict_writer.writerow(l)
                
        Logger.debug('prep_files: Arquivo %s_%s criado.' % (prefixo, arquivo))
    except (IOError, TypeError, csv.Error) as e:
        Logger.error('prep_files: Erro ao criar arquivo: %s' % e)


def _identifica_diretorio(caminho_completo):
    try:
        arquivo = os.path.basename(caminho_completo)
        diretorio = os.path.dirname(caminho_completo)
        Logger.debug("prep_geocode: %s, %s" % (diretorio, arquivo))
        return diretorio, arquivo
    except Exception as e:
        Logger.error('Erro ao manipular o diretório: %s' % e)

def zip_files(nome_arquivo):
    '''

    '''
    try:
        arquivo = nome_arquivo.replace('.csv', '')
        diretorio = diretorio_saida + 'files_' + arquivo + '/'
        arquivo_zip = diretorio + arquivo + '.zip'

        zip_file = zipfile.ZipFile(arquivo_zip, 'w')

        for folder, subfolders, files in os.walk(diretorio):

            for file in files:
                if file.endswith('.csv'):
                    zip_file.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), diretorio), compress_type = zipfile.ZIP_DEFLATED)

        zip_file.close()

        Logger.debug('prep_files: ' + nome_arquivo.replace('.csv', '.zip') + ' criado.')
        return arquivo_zip

    except Exception as e:
        Logger.error('prep_files: Erro ao criar arquivo zip: %s' % e)
