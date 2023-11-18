import paho.mqtt.client as mqtt

broker_address = "localhost"
port = 1883
topic = "atuador/status"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao servidor MQTT")
        client.subscribe(topic)
    else:
        print(f"Falha na conexão ao servidor MQTT com código de retorno {rc}")

def on_message(client, userdata, msg):
    print("Mensagem recebida:")
    print(f"Tópico: {msg.topic}")
    print(f"Mensagem: {msg.payload.decode()}")
    print(f"QoS: {msg.qos}")
    print(f"Retained: {msg.retain}")
    print("------")

    if msg.payload.decode() == "ativado":
        print("Alarme ativado, Email enviado")

if __name__ == "__main__":
    print("Iniciando atuador")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_address, port, 60)
    print("Conectado ao servidor MQTT")
    
    client.loop_forever()
