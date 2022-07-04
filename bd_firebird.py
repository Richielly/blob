import fdb
import io

def insert_blob_firebird():
    con = fdb.connect(dsn='localhost:D:\Conversao\Frotas\ManoelRibas\Banco\EQUIPLANO.FDB', user='sysdba', password='masterkey')

    cur = con.cursor()

    f = open('C:\\Users\\Equiplano\\Desktop\\teste_blob\\2022\\images.jpg', 'rb')
    # cur.execute('insert into entidade (CNPJ,CARGOREPRESENTANTELEGAL,CEP,BAIRRO,NUMERO,TIPOPREVIDENCIA,CODESFERAGOVERNO, CODREPRESENTANTELEGAL,TIPOENTIDADE, CODCIDADE, CODENTIDADE,LOGRADOURO, nome, IMAGEMBRASAO) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
    #             ['76030717000148','Presidente','81770125','Centro',99,1,5,1,2,3,100, 'LOGRADOURO','nome',f])

    cur.execute('update entidade set IMAGEMBRASAO = (?)', [f])

    f.close()

    con.commit()

    con.close()
insert_blob_firebird()