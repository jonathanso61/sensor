import paho.mqtt.client as mqtt

broker_address = "localhost"
port = 1883
topic = "atuador/status"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao servidor MQTT")
    else:
        print(f"Falha na conexão ao servidor MQTT com código de retorno {rc}")

def on_message(client, userdata, msg):
    status = msg.payload.decode()
    print(f"Atuador - Status recebido: {status}")

    if status == "ativado":
        print("Alarme ativado")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_address, port, 60)
    client.subscribe(topic)

    client.loop_forever()
