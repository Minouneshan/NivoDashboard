'''
Button Click 
'''
# Button click event
from clickhouse_driver import Client
from kafka import KafkaConsumer, TopicPartition
import json
from datetime import datetime
client = Client(host='localhost', password='password', database='V1')


consumer = KafkaConsumer(
    'buttonclick',
    bootstrap_servers=['localhost:9092'])
for message in consumer:
    button_click = {}
    message = message.value
    message = message.decode('ascii')
    print(message)
    button_click = json.loads(message)
    print(button_click)
    client.execute(
        'insert into user_button_click (token,button_name,datetime,time) values ', [[button_click['token'], button_click['button_name'], datetime.fromtimestamp(button_click['time']),datetime.fromtimestamp(button_click['time'])]])

