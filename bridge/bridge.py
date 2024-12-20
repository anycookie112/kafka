import paho.mqtt.client as mqtt
from pykafka import KafkaClient
import time

mqtt_broker = "192.168.1.15"
mqtt_client = mqtt.Client("mqtt", clean_session=True)  # Remove callback_api_version


kafka_client = KafkaClient(hosts="localhost:9092")
kafka_topic = kafka_client.topics['device_state']
kafka_producer = kafka_topic.get_sync_producer()

def on_message(client, userdata, message):
    msg_payload = str(message.payload.decode())  # Decoding payload to string
    print("Received MQTT message: ", msg_payload)
    kafka_producer.produce(msg_payload.encode('ascii'))
    print("KAFKA: Just published " + msg_payload + " to topic device_state")

# Assign the callback function
mqtt_client.on_message = on_message

# Connect to MQTT Broker
mqtt_client.connect(mqtt_broker)

# Subscribe to the desired topic
mqtt_client.subscribe("device/state")

# Start the MQTT client loop in a separate thread
mqtt_client.loop_start()

# Keep the script running to allow message handling
try:
    while True:
        time.sleep(1)  # Main thread can be idle here while MQTT loop runs
except KeyboardInterrupt:
    print("Exiting...")
    mqtt_client.loop_stop()
