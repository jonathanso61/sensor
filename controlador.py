import paho.mqtt.client as mqtt
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

broker_address = "localhost"
port = 1883
sensor_topic = "sensor/movimento"
atuador_topic = "atuador/status"
backup_topic = "atuador/status/backup"

mongo1_uri = "mongodb://localhost:27017/"
mongo2_uri = "mongodb://localhost:27017/"

def connect_mongo():
    try:
        client = MongoClient(mongo1_uri)
        client.admin.command('ismaster')  # Check if the server is available
        return client
    except ConnectionFailure:
        print("Falha na conexão com MongoDB 1. Tentando MongoDB 2...")
        return MongoClient(mongo2_uri)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao servidor MQTT")
        client.subscribe(sensor_topic)
    else:
        print(f"Falha na conexão ao servidor MQTT com código de retorno {rc}")

def on_message(client, userdata, msg):
    valor = int(msg.payload.decode())
    print(f"Controlador 1 - Valor recebido: {valor}")

    # Tomar decisão com base no valor
    if valor == 1:
        # Ativar o código do atuador 1 aqui
        client.publish(atuador_topic, "ativado")
        # Publicar também no tópico de backup
        client.publish(backup_topic, "ativado")

        # Salvar dados no MongoDB
        mongo_client = connect_mongo()
        db = mongo_client["movimento_db1"]
        collection = db["movimento_collection1"]
        collection.insert_one({"valor": valor})

        print(mongo_client.list_database_names())

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_address, port, 60)

    client.loop_forever()



