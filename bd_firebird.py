import fdb
import os
import base64
import configparser

cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

def write_binario(data, filename):

    with open(filename, "wb") as file:
        try:
            if isinstance(data, bytes):
                file.write(data)
            else:
                print(type(data))
                file.write(data.read())
        except: "Erro inesperado."


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

def extract_blob(path, resp):
    count = 0
    for png in resp:

        file = criarDiretorioArquivo_png(path, png[0], png[1], png[2], png[3])
        # print('**************************************')
        # print(file)
        count += 1

def insert_blob_firebird():

    f = open('C:\\Users\\Equiplano\\Desktop\\teste_blob\\2022\\images.jpg', 'rb')
    # cur.execute('insert into entidade (CNPJ,CARGOREPRESENTANTELEGAL,CEP,BAIRRO,NUMERO,TIPOPREVIDENCIA,CODESFERAGOVERNO, CODREPRESENTANTELEGAL,TIPOENTIDADE, CODCIDADE, CODENTIDADE,LOGRADOURO, nome, IMAGEMBRASAO) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
    #             ['76030717000148','Presidente','81770125','Centro',99,1,5,1,2,3,100, 'LOGRADOURO','nome',f])

    con = fdb.connect(dsn='localhost:D:\ArquivosBlob\EQUIPLANO.GDB', user='sysdba', password='masterkey')
    cur = con.cursor()

    cur.execute('update entidade set IMAGEMBRASAO = (?)', [f])
    f.close()
    con.commit()
    con.close()

def start ():

    con = fdb.connect(dsn='localhost:D:\ArquivosBlob\EQUIPLANO.GDB', user='sysdba', password='masterkey')
    cur = con.cursor()

    sql = 'select pi.codentidade, pi.codpessoafisica, pi.nmimagem, pi.arquivo from SRH_PESSOAFISICAIMAGEM pi where arquivo is not null'
    cur.execute(sql)
    resp = cur.fetchall()

    # for i in resp:
    #     print(i)
    #     print('\n\n')

    extract_blob(cfg['DEFAULT']['Path'], resp)

start()