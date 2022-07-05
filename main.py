import cx_Oracle
import os
# import uuid
import base64
import configparser
# import secrets

# secrets.token_hex(16)

# oracledb.init_oracle_client()
cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

def write_blob():

    with open('C:\\Users\\Equiplano\\Desktop\\teste_blob\\2022\\teste.pdf', 'rb') as f:
        blob = base64.b64encode(f.read())
    text_file = open('C:\\Users\\Equiplano\\Desktop\\teste_blob\\2022\\teste.txt', "wb")
    text_file.write(blob)
    text_file.close()
    with open('C:\\Users\\Equiplano\\Desktop\\teste_blob\\2022\\teste.txt', 'r') as f:
        blob = f.read()
    blob = base64.b64decode(blob)
    text_file = open('C:\\Users\\Equiplano\\Desktop\\teste_blob\\2022\\result.pdf', 'wb')
    text_file.write(blob)
    text_file.close()

    return blob

def conectarOracle(schema, password, host, servicName):
    url = schema + '/' + password + '@' + host + '/' + servicName
    connection = cx_Oracle.connect(url)
    # print('Conectando no Oracle! ' + connection.version)
    return connection

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

def write_file_png(data, filename):
    with open(filename, 'rb') as f:
        f.write(data)

def write_binario(data, filename):
    with open(filename, "wb") as file:
        file.write(data)

def binario_to_png(binario):
    file = open(binario, 'rb')
    byte = file.read()
    file.close()

    decodeit = open('hello_level.jpeg', 'wb')
    decodeit.write(base64.b64decode((byte)))
    decodeit.close()

def convertData(filename):
    # Convert images or files data to binary format
    with open(filename, 'rb', encoding='latin-1') as file:
        binary_data = file.read()

    return binary_data

# def criarDiretorioArquivo(path, ano, data):
#
#     caminho = path + '\\' + ano + '\\'
#     arquivo = caminho + str(uuid.uuid1()) + '.png'
#     # arquivo = caminho + str(uuid.uuid1()) + '.pdf'
#     if not os.path.exists(caminho):
#         os.makedirs(caminho)
#     if not os.path.exists(arquivo):
#         #write_file(data, arquivo) # Pdf
#         write_binario(data, arquivo)
#         return arquivo

def criarDiretorioArquivo_png(path, entidade, cod_pessoa, extensao, data):

    caminho = path + '\\' + str(entidade) + '\\'

    ext = str(extensao).split('.')
    ext = ext[-1]
    nome = str(extensao).replace('.' + ext, '')

    arquivo = caminho + str(entidade) + '-' + str(cod_pessoa) + '-' + str(nome) + f'.{ext}'
    if not os.path.exists(caminho):
        os.makedirs(caminho)
    if not os.path.exists(arquivo):
        write_binario(data, arquivo)
        return arquivo

# def extrair_arquivos_pdf(path, resp):
#     count = 0
#
#     for pdf in resp:
#         file = criarDiretorioArquivo(path, "2022", pdf[0].read())
#         print('**************************************')
#         print(file)
#         count += 1
#     print('******************************************')
#     print('Total de arquivos migrados: ', count)

def extrair_arquivos_png(path, resp):
    count = 0

    for png in resp:
        # print(png)
        file = criarDiretorioArquivo_png(path, png[0], png[1], png[2], png[3].read())
        # print('**************************************')
        # print(file)
        count += 1
    # print('******************************************')
    # print('Total de arquivos migrados: ', count)

def main():

    # path = input('Digite a pasta: ')

    # print('**************************************')
    con = conectarOracle(cfg['DEFAULT']['User'], cfg['DEFAULT']['Password'], cfg['DEFAULT']['Host'], cfg['DEFAULT']['Service'])
    cur = con.cursor()
    sql = 'select pi.codentidade, pi.codpessoafisica, pi.nmimagem, pi.arquivo from SRH_PESSOAFISICAIMAGEM pi where arquivo is not null'
    resp = cur.execute(sql)

    extrair_arquivos_png(cfg['DEFAULT']['Path'], resp)

# if __name__ == '__main__':
main()
# pyinstaller --name ExtractBlob --onefile --console main.py