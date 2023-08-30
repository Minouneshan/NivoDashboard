
#2
# consumer
from clickhouse_driver import Client
from kafka import KafkaConsumer, TopicPartition
import json
from datetime import datetime
client = Client(host='localhost', password='password', database='V1')


consumer = KafkaConsumer(
    'event',
    bootstrap_servers=['localhost:9092'])
for message in consumer:
    event = {}
    message = message.value
    message = message.decode('ascii')
    print(message)
    event = json.loads(message)
    print(event)
    client.execute(
        'insert into user_event (token,event_name,datetime,time,metadata) values ', [[event['token'], event['event_name'], datetime.fromtimestamp(event['time']),datetime.fromtimestamp(event['time']), event['metadata']]])

