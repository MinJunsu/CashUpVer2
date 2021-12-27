from datetime import timedelta, datetime
import requests

from bitmex.models import MainHourData, SubHourData, ThirdHourData, MainMinuteData, SubMinuteData, ThirdMinuteData


class BitmexRealTimeData:
    COUNT = 10
    symbols = {
        '1h': [
            {
                'symbol': 'XBTUSD',
                'obj': MainHourData,
            },
            {
                'symbol': 'XBTEUR',
                'obj': SubHourData,
            },
            {
                'symbol': 'XBTM22',
                'obj': ThirdHourData
            }
        ],
        '5m': [
            {
                'symbol': 'XBTUSD',
                'obj': MainMinuteData
            },
            {
                'symbol': 'XBTEUR',
                'obj': SubMinuteData
            },
            {
                'symbol': 'XBTM22',
                'obj': ThirdMinuteData
            }
        ]
    }

    def get_data(self, symbol, bins, model):
        URL = f'https://www.bitmex.com/api/v1/trade/bucketed?symbol={symbol}&binSize={bins}&partial=true&&count=10&reverse=true'

        response = requests.get(URL).json()
        for element in reversed(response):
            if bins == '1h':
                timestamp = datetime.strptime(element['timestamp'].replace("T", " ")[0:19],
                                              "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)
            else:
                timestamp = datetime.strptime(element['timestamp'].replace("T", " ")[0:19],
                                              "%Y-%m-%d %H:%M:%S") + timedelta(hours=9) - timedelta(minutes=5)

            open_price = element['open'] if element['open'] is not None else 0
            high_price = element['high'] if element['high'] is not None else 0
            low_price = element['low'] if element['low'] is not None else 0
            close_price = element['close'] if element['close'] is not None else 0
            volume = element['volume'] if element['volume'] is not None else 0
            obj = model()

            obj.time = f"{str(timestamp.day).zfill(2)} {str(timestamp.hour).zfill(2)}:{str(timestamp.minute).zfill(2)}"
            obj.min_price = low_price
            obj.max_price = high_price
            obj.open_price = open_price
            obj.close_price = close_price
            obj.volume = volume
            obj.datetime = timestamp
            obj.save()

    def run(self):
        hour_symbols = self.symbols['1h']
        for hour in hour_symbols:
            symbol = hour['symbol']
            model = hour['obj']
            bins = '1h'
            self.get_data(symbol, bins, model)

        minute_symbols = self.symbols['5m']
        for minute in minute_symbols:
            symbol = minute['symbol']
            model = minute['obj']
            bins = '5m'
            self.get_data(symbol, bins, model)




class BitmexBackData:
    COUNT = 1000
    BASE_URL = 'https://www.bitmex.com/api/v1/'
    symbols = {
        '1h': [
            {
                'start': 54000,
                'symbol': 'XBTUSD',
                'obj': MainHourData,
            },
            {
                'start': 3600,
                'symbol': 'XBTEUR',
                'obj': SubHourData,
            },
            {
                'start': 0,
                'symbol': 'XBTM22',
                'obj': ThirdHourData
            }
        ],
        '5m': [
            {
                'start': 645000,
                'symbol': 'XBTUSD',
                'obj': MainMinuteData
            },
            {
                'start': 42000,
                'symbol': 'XBTEUR',
                'obj': SubMinuteData
            },
            {
                'start': 0,
                'symbol': 'XBTM22',
                'obj': ThirdMinuteData
            }
        ]
    }

    def __init__(self):
        self.path = '/trade/bucketed/'
        self.URL = self.BASE_URL + self.path

    def get_back_data(self, symbol, model, bins, start):
        URL = f'https://www.bitmex.com/api/v1/trade/bucketed?symbol={symbol}&binSize={bins}&partial=true&start={start}&count=1000&reverse=false'
        response = requests.get(URL).json()

        for element in response:
            if bins == '1h':
                timestamp = datetime.strptime(element['timestamp'].replace("T", " ")[0:19],
                                              "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)
            else:
                timestamp = datetime.strptime(element['timestamp'].replace("T", " ")[0:19],
                                              "%Y-%m-%d %H:%M:%S") + timedelta(hours=9) - timedelta(minutes=5)

            open_price = element['open'] if element['open'] is not None else 0
            high_price = element['high'] if element['high'] is not None else 0
            low_price = element['low'] if element['low'] is not None else 0
            close_price = element['close'] if element['close'] is not None else 0
            volume = element['volume'] if element['volume'] is not None else 0
            obj = model()

            obj.time = f"{str(timestamp.day).zfill(2)} {str(timestamp.hour).zfill(2)}:{str(timestamp.minute).zfill(2)}"
            obj.min_price = low_price
            obj.max_price = high_price
            obj.open_price = open_price
            obj.close_price = close_price
            obj.volume = volume
            obj.datetime = timestamp
            obj.save()

        if len(response) < 1000:
            return False
        return True

    def run(self):
        hour_symbols = self.symbols['1h']
        for hour in hour_symbols:
            start = hour['start']
            while self.get_back_data(symbol=hour['symbol'], model=hour['obj'], bins='1h', start=start):
                start += 1000

        minute_symbols = self.symbols['5m']
        for minute in minute_symbols:
            start = minute['start']
            while self.get_back_data(symbol=minute['symbol'], model=minute['obj'], bins='5m', start=start):
                start += 1000
