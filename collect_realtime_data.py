import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'CashUpVer2.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

import django
import sys
django.setup()

from bitmex.models import RealTimeData
import websocket
import json
from datetime import datetime, timedelta

query = RealTimeData.objects.filter(market="BitMEX")
usd = query.filter(symbol='XBTUSD').last()
eur = query.filter(symbol='XBTEUR').last()
m22 = query.filter(symbol='XBTM22').last()

initial_time = datetime.now()


def on_message(ws, message):
    message = json.loads(message)
    action = message.get("action")
    data = message.get("data")[0]
    print(message)
    if action == "insert":
        if data['symbol'] == "XBTUSD":
            usd.close_price = data['price']

        elif data['symbol'] == "XBTEUR":
            eur.close_price = data['price']
        else:
            m22.close_price = data['price']

        if datetime.now() - initial_time > timedelta(minutes=5):
            ws.close()
    else:
        if data['symbol'] == "XBTUSD":
            usd.bid_price = data['bids'][0][0]
            usd.ask_price = data['asks'][0][0]
        elif data['symbol'] == "XBTEUR":
            eur.bid_price = data['bids'][0][0]
            eur.ask_price = data['asks'][0][0]
        else:
            m22.bid_price = data['bids'][0][0]
            m22.ask_price = data['asks'][0][0]

    usd.save()
    eur.save()
    m22.save()


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    ws.send('{"op": "subscribe", "args": ["trade:XBTUSD"]}')
    ws.send('{"op": "subscribe", "args": ["trade:XBTEUR"]}')
    ws.send('{"op": "subscribe", "args": ["trade:XBTM22"]}')
    ws.send('{"op": "subscribe", "args": ["orderBook10:XBTUSD"]}')
    ws.send('{"op": "subscribe", "args": ["orderBook10:XBTEUR"]}')
    ws.send('{"op": "subscribe", "args": ["orderBook10:XBTM22"]}')


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://www.bitmex.com/realtime",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()