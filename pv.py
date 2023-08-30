'''
page view 
'''
# consumer page view event
from clickhouse_driver import Client
from kafka import KafkaConsumer, TopicPartition
from datetime import datetime
import json
client = Client(host='localhost', password='password', database='V1')


consumer = KafkaConsumer(
    'pageview',
    bootstrap_servers=['localhost:9092'])
for message in consumer:
    page_view={}
    message = message.value
    message = message.decode('ascii')
    print(message)
    page_view = json.loads(message)
    print(page_view)
    client.execute(
        'insert into user_page_view (token,page_name,datetime,time) values ', [[page_view['token'], page_view['page_name'],datetime.fromtimestamp(page_view['time']),datetime.fromtimestamp(page_view['time'])]])
    #    client.execute(message.decode('ascii'))

