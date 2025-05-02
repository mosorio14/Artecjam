import serial
import mysql.connector
import time
from datetime import datetime

# Configuração da porta serial (ajuste conforme necessário)
porta_serial = 'COM3'  # Ex: 'COM3' no Windows, '/dev/ttyUSB0' no Linux
baud_rate = 9600

# Conexão com o Arduino
try:
    arduino = serial.Serial(porta_serial, baud_rate, timeout=2)
    print(f'Conectado ao Arduino na porta {porta_serial}')
    time.sleep(2)  # Tempo para estabilizar conexão
except Exception as e:
    print(f'Erro ao conectar com a porta serial: {e}')
    exit(1)

# Conexão com o banco de dados SingleStore (MySQL)
def conectar_banco():
    return mysql.connector.connect(
        host='svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com',
        port='3333',
        user='ARTECJAM',
        password='u)eKirme27uyE8xFxp=id',
        database='db_mariana_676af'
    )

def inserir_dados(sujeira):
    try:
        dados = []
        conn = conectar_banco()
        cursor = conn.cursor()
        hora = (datetime.now()).time()  # random time between 5:00 and 20:00
        data = (datetime.today()).date()
        eficiencia = 100-sujeira
        dados.append((hora, data, sujeira, eficiencia))

        query = """
        INSERT INTO dadosDummySHIFT (hora, data, sujeira, eficiencia)
        VALUES (%s, %s, %s, %s)
        """

        cursor.executemany(query, dados)
        conn.commit()

        print(f"✅ {cursor.rowcount} registros inseridos com sucesso na tabela 'dadosDummySHIFT'.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Erro ao inserir dados: {err}")


from datetime import time as time_obj  # for time comparison

# Loop principal
while True:
    try:
        linha = arduino.readline().decode('utf-8').strip()
        if linha:
            print(f"Recebido do Arduino: {linha}")
            valor = int(linha)

            agora = datetime.now().time()
            # Verifica se está entre 00:00 e 03:00
            if time_obj(0, 0) <= agora <= time_obj(20, 0):
                inserir_dados(valor)
    except ValueError:
        print("Valor inválido recebido.")
    except KeyboardInterrupt:
        print("Encerrando...")
        break
