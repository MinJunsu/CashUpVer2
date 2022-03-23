import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'CashUpVer2.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"

import django
import sys
django.setup()

from bitmex.models import RealTimeData
import websocket
import threading
import json
from datetime import datetime, timedelta

query = RealTimeData.objects.filter(market="BitMEX")
usd = query.filter(symbol='XBTUSD').last()
eur = query.filter(symbol='XBTEUR').last()
h22 = query.filter(symbol='XBTH22').last()
m22 = query.filter(symbol='XBTM22').last()

usd_price, usd_bid_price, usd_ask_price = usd.close_price, usd.bid_price, usd.ask_price
eur_price, eur_bid_price, eur_ask_price = eur.close_price, eur.bid_price, eur.ask_price
h22_price, h22_bid_price, h22_ask_price = h22.close_price, h22.bid_price, h22.ask_price
m22_price, m22_bid_price, m22_ask_price = m22.close_price, m22.bid_price, m22.ask_price

initial_time = datetime.now()


def on_message_trade(ws, message):
    global usd_ask_price, usd_bid_price, usd_price, eur_price, eur_bid_price, eur_ask_price, h22_price, h22_bid_price, h22_ask_price, m22_price, m22_bid_price, m22_ask_price
    message = json.loads(message)
    data = message.get("data")[0]

    if data['symbol'] == "XBTUSD":
        usd_price = data['price']

    elif data['symbol'] == "XBTEUR":
        eur_price = data['price']

    elif data['symbol'] == 'XBTH22':
        h22_price = data['price']

    else:
        m22_price = data['price']

    if datetime.now() - initial_time > timedelta(minutes=6):
        ws.close()

    usd.close_price = usd_price
    eur.close_price = eur_price
    h22.close_price = h22_price
    m22.close_price = m22_price

    usd.save()
    eur.save()
    h22.save()
    m22.save()


def on_message_order(ws, message):
    global usd_ask_price, usd_bid_price, usd_price, eur_price, eur_bid_price, eur_ask_price, h22_price, h22_bid_price, h22_ask_price, m22_price, m22_bid_price, m22_ask_price
    message = json.loads(message)
    data = message.get("data")[0]

    if data['symbol'] == "XBTUSD":
        usd_bid_price = data['bids'][0][0]
        usd_ask_price = data['asks'][0][0]

    elif data['symbol'] == "XBTEUR":
        eur_bid_price = data['bids'][0][0]
        eur_ask_price = data['asks'][0][0]

    elif data['symbol'] == "XBTH22":
        h22_bid_price = data['bids'][0][0]
        h22_ask_price = data['asks'][0][0]

    else:
        m22_bid_price = data['bids'][0][0]
        m22_ask_price = data['asks'][0][0]

    if datetime.now() - initial_time > timedelta(minutes=6):
        ws.close()

    usd.bid_price = usd_bid_price
    usd.ask_price = usd_ask_price

    eur.bid_price = eur_bid_price
    eur.ask_price = eur_ask_price

    h22.bid_price = h22_bid_price
    h22.ask_price = h22_ask_price

    m22.bid_price = m22_bid_price
    m22.ask_price = m22_ask_price

    usd.save()
    eur.save()
    h22.save()
    m22.save()


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open_trade(ws):
    ws.send('{"op": "subscribe", "args": ["trade:XBTUSD"]}')
    ws.send('{"op": "subscribe", "args": ["trade:XBTEUR"]}')
    ws.send('{"op": "subscribe", "args": ["trade:XBTH22"]}')
    ws.send('{"op": "subscribe", "args": ["trade:XBTM22"]}')


def on_open_order(ws):
    ws.send('{"op": "subscribe", "args": ["orderBook10:XBTUSD"]}')
    ws.send('{"op": "subscribe", "args": ["orderBook10:XBTEUR"]}')
    ws.send('{"op": "subscribe", "args": ["orderBook10:XBTH22"]}')
    ws.send('{"op": "subscribe", "args": ["orderBook10:XBTM22"]}')


def create_websocket(flag):
    websocket.enableTrace(False)
    if flag:
        ws_trade = websocket.WebSocketApp("wss://www.bitmex.com/realtime",
                                          on_open=on_open_trade,
                                          on_message=on_message_trade,
                                          on_error=on_error,
                                          on_close=on_close)
        ws_trade.run_forever()

    else:
        ws_order = websocket.WebSocketApp("wss://www.bitmex.com/realtime",
                                          on_open=on_open_order,
                                          on_message=on_message_order,
                                          on_error=on_error,
                                          on_close=on_close)
        ws_order.run_forever()


if __name__ == '__main__':
    t1 = threading.Thread(target=create_websocket, args=[True])
    t2 = threading.Thread(target=create_websocket, args=[False])

    t1.start()
    t2.start()
