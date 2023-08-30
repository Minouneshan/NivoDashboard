# producer
import json
from datetime import datetime
import sys
from flask import Flask, jsonify, abort, make_response, request, url_for
import uuid
from kafka import SimpleProducer, KafkaClient
from flask_clickhouse import ClickHouse
sample = Flask(__name__)
sample.config['CLICKHOUSE_USER'] = 'default'
sample.config['CLICKHOUSE_PASSWORD'] = '0020520107'
sample.config['CLICKHOUSE_DATABASE'] = 'V1'
sample.config['CLICKHOUSE_HOST'] = 'localhost'
ch = ClickHouse(sample)

try:

    Kafka = KafkaClient('localhost:9092')
    producer = SimpleProducer(Kafka)
except:
    print("error in creating clientntt", file=sys.stdout)
    f = open("err.txt", "w+")
    f.write("error happened")
    f.close()


@sample.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@sample.route('/api/v1/get_token', methods=['POST'])
def user_get_token():
    if not request.json or not 'user_id' in request.json:
        return jsonify({'status': 0,
                        'message': 'user_id is empty',
                        'data': ''})

    if not request.json or not 'time' in request.json:
        return jsonify({'status': 0,
                        'message': 'time is empty',
                        'data': ''})
    token = str(uuid.uuid1())
    try:
        get_token = {
            'user_id': request.json['user_id'],
            'wallet_id': request.json.get('wallet_id', ""),
            'device_model': request.json.get('page_name', ""),
            'time': datetime.fromtimestamp(float(request.json['time'])),
            'os': request.json.get('os', ""),
            'os_version': request.json.get('os_version', ""),
            'app_version': request.json.get('app_version', ""),
            'package_name': request.json.get('package_name', ""),
            'market_place': request.json.get('market_place', ""),
            'metadata': request.json.get('metadata', ""),
        }
        ch.execute('insert into user_get_token (user_id,device_model,datetime,time,os,os_version,app_version,package_name,market_place,metadata,token) values', [
            [get_token['user_id'], get_token['device_model'], get_token['time'], get_token['time'], get_token['os'], get_token['os_version'], get_token['app_version'], get_token['package_name'], get_token['market_place'], get_token['metadata'], token]])

        return jsonify({'status': 1,
                        'data': '',
                        'token': token}), 201
    except Exception as e:
        print(e, file=sys.stderr)
        return jsonify({'status': 0,
                        'data': ''})


@sample.route('/api/v1/get_token_batch_insertion', methods=['POST'])
def user_get_token_batch_insertion():
    if not request.json or not 'user_id' in request.json:
        return jsonify({'status': 0,
                        'message': 'user_id is empty',
                        'data': ''})

    if not request.json or not 'time' in request.json:
        return jsonify({'status': 0,
                        'message': 'time is empty',
                        'data': ''})

    try:
        get_token = {
            'user_id': request.json['user_id'],
            'wallet_id': request.json.get('wallet_id', ""),
            'device_model': request.json.get('page_name', ""),
            'time': datetime.fromtimestamp(float(request.json['time'])),
            'os': request.json.get('os', ""),
            'os_version': request.json.get('os_version', ""),
            'app_version': request.json.get('app_version', ""),
            'package_name': request.json.get('package_name', ""),
            'market_place': request.json.get('market_place', ""),
            'token_count': request.json.get('token_count', ""),
            'metadata': request.json.get('metadata', ""),
        }

        token_list = []
        for i in range(get_token['token_count']):
            token_list.append(str(uuid.uuid1()))
            ch.execute('insert into user_get_token (user_id,device_model,datetime,time,os,os_version,app_version,package_name,market_place,metadata,token) values', [
                [get_token['user_id'], get_token['device_model'], get_token['time'], get_token['time'], get_token['os'], get_token['os_version'], get_token['app_version'], get_token['package_name'], get_token['market_place'], get_token['metadata'], token_list[i]]])

        return jsonify({'status': 1,
                        'data': '',
                        'token_list': token_list}), 201
    except Exception as e:
        print(e, file=sys.stderr)
        return jsonify({'status': 0,
                        'data': ''})


@sample.route('/api/v1/view', methods=['POST'])
def user_page_views():
    print(request.json, file=sys.stdout)

    if not request.json or not 'token' in request.json:
        return jsonify({'status': 0,
                        'message': 'token is empty',
                        'data': ''})

    if not request.json or not 'time' in request.json:
        return jsonify({'status': 0,
                        'message': 'time is empty',
                        'data': ''})

    try:
        page_view = {
            'token': request.json['token'],
            'page_name': request.json.get('page_name', ""),
            'time': float(request.json['time']),
        }

        page_view_request = json.dumps(page_view)
        producer.send_messages('pageview', page_view_request.encode('ascii'))
        return jsonify({'status': 1,
                        'data': ''}), 201
    except Exception as e:
        print(e, file=sys.stderr)
        return jsonify({'status': 0,
                        'data': ''})


@sample.route('/api/v1/button', methods=['POST'])
def user_button_clicks():
    if not request.json or not 'token' in request.json:
        return jsonify({'status': 0,
                        'message': 'token is empty',
                        'data': ''})
    if not request.json or not 'time' in request.json:
        return jsonify({'status': 0,
                        'message': 'time is empty',
                        'data': ''})
    try:
        button_click = {
            'token': request.json['token'],
            'button_name': request.json.get('button_name', ""),
            'time': float(request.json['time']),
        }

        button_click_request = json.dumps(button_click)
        producer.send_messages('buttonclick',
                               button_click_request.encode('ascii'))
        return jsonify({'status': 1,
                        'data': ''}), 201
    except:
        return jsonify({'status': 0,
                        'data': ''})


@sample.route('/api/v1/event', methods=['POST'])
def user_events():
    if not request.json or not 'token' in request.json:
        return jsonify({'status': 0,
                        'message': 'token is empty',
                        'data': ''})
    if not request.json or not 'time' in request.json:
        return jsonify({'status': 0,
                        'message': 'time is empty',
                        'data': ''})
    try:
        event = {
            'token': request.json['token'],
            'event_name': request.json.get('event_name', ""),
            'time': float(request.json['timestamp']),
            'metadata': request.json.get('metadata', ""),
        }

        event_request = json.dumps(event)
        producer.send_messages('event',
                               event_request.encode('ascii'))
        return jsonify({'status': 1,
                        'data': ''}), 201
    except:
        return jsonify({'status': 0,
                        'data': ''})


@sample.route('/api/v1/batch_insertion', methods=['POST'])
def batch_insertion():
    batch = request.json['data']
    try:
        for req in batch:
            print(req, file=sys.stdout)
            if req['api'] == 'page_view':
                d = req['data']
                if d['token'] == "":
                    return jsonify({'status': 0,
                                    'message': 'token is empty',
                                    'data': ''})
                if d['time'] == "":
                    return jsonify({'status': 0,
                                    'message': 'time is empty',
                                    'data': ''})

                page_view = {
                    'token': d['token'],
                    'page_name': d['page_name'],
                    'time': float(d['time']),
                }

                page_view_request = json.dumps(page_view)
                producer.send_messages(
                    'pageview', page_view_request.encode('ascii'))
            elif req['api'] == 'button_click':
                d = req['data']
                if d['token'] == "":
                    return jsonify({'status': 0,
                                    'message': 'token is empty',
                                    'data': ''})
                if d['time'] == "":
                    return jsonify({'status': 0,
                                    'message': 'time is empty',
                                    'data': ''})
                button_click = {
                    'token': d['token'],
                    'button_name': d['button_name'],
                    'time': float(d['time']),
                }

                button_click_request = json.dumps(button_click)
                producer.send_messages('buttonclick',
                                       button_click_request.encode('ascii'))
            else:
                d = req['data']
                if d['token'] == "":
                    return jsonify({'status': 0,
                                    'message': 'token is empty',
                                    'data': ''})
                if d['time'] == "":
                    return jsonify({'status': 0,
                                    'message': 'time is empty',
                                    'data': ''})
                event = {
                    'token': d['token'],
                    'event_name': d['event_name'],
                    'time': float(d['time']),
                    'metadata': d['metadata'],
                }
                event_request = json.dumps(event)
                producer.send_messages('event',
                                       event_request.encode('ascii'))

        return jsonify({'status': 1,
                        'data': ''}), 201

    except:
        return jsonify({'status': 0,
                        'data': ''})


if __name__ == '__main__':
    sample.run(debug=True, host='0.0.0.0')
