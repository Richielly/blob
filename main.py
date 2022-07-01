import oracledb
import os
import uuid
import base64

oracledb.init_oracle_client()

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
    connection = oracledb.connect(url)
    print('Conectando no Oracle! ' + connection.version)
    return connection

def write_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(data)

def convertData(filename):
    # Convert images or files data to binary format
    with open(filename, 'rb', encoding='latin-1') as file:
        binary_data = file.read()

    return binary_data

def criarDiretorioArquivo(path, ano, data):

    caminho = path + '\\' + ano + '\\'
    arquivo = caminho + str(uuid.uuid1()) + '.pdf'
    if not os.path.exists(caminho):
        os.makedirs(caminho)
    if not os.path.exists(arquivo):
        write_file(data, arquivo)
        return arquivo

def main():

    path = input('Digite a pasta: ')

    print('**************************************')
    con = conectarOracle('NFSPRODUCAO', 'bdesp1974', 'localhost', 'eqplano')
    cur = con.cursor()
    sql = 'select pdfnota from copianotaimagem'
    resp = cur.execute(sql)

    count = 0

    for pdf in resp:
        file = criarDiretorioArquivo(path, "2022", pdf[0].read())
        print('**************************************')
        print(file)
        count+=1
    print('******************************************')
    print('Total de arquivos migrados: ', count)

if __name__ == '__main__':
    main()
