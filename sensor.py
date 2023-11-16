import random
import time
import paho.mqtt.client as mqtt

# Configurações do servidor MQTT
broker_address = "localhost"  # Endereço do servidor MQTT
port = 1883  # Porta padrão do MQTT
topic = "sensor/movimento"  # Tópico para enviar os valores do sensor

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao servidor MQTT")
    else:
        print(f"Falha na conexão ao servidor MQTT com código de retorno {rc}")

def sensor_movimento(client):
    while True:
        # Gera um valor aleatório de 0 ou 1 para simular o sensor de movimento
        valor = random.randint(0, 1)
        
        # Publica o valor no tópico MQTT
        client.publish(topic, str(valor))
        
        # Verifica se o valor é 1 (movimento detectado)
        if valor == 1:
            print("Movimento detectado!")
        else:
            print("Nenhum movimento detectado.")
        
        # Aguarda 5 segundos antes de gerar o próximo valor
        time.sleep(5)

if __name__ == "__main__":
    # Configura o cliente MQTT
    client = mqtt.Client()
    client.on_connect = on_connect

    # Conecta ao servidor MQTT
    client.connect(broker_address, port, 60)

    # Inicia um thread para processar a comunicação MQTT em segundo plano
    client.loop_start()

    try:
        # Inicia o sensor de movimento
        sensor_movimento(client)
    except KeyboardInterrupt:
        # Encerra a execução do programa quando o usuário pressiona Ctrl + C
        print("Programa encerrado pelo usuário")

    # Desconecta do servidor MQTT ao finalizar o programa
    client.disconnect()

