from datetime import timedelta, datetime
import requests

from bitmex.models import MainHourData, SubHourData, ThirdHourData, MainMinuteData, SubMinuteData, ThirdMinuteData


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
        response = requests.get(self.URL, params={
            'symbol': symbol,
            'binSize': bins,
            'partial': False,
            'start': start,
            'count': self.COUNT,
            'reverse': True
        }).json()
        for element in response:
            if bins == '1h':
                timestamp = datetime.strptime(element['timestamp'].replace("T", " ")[0:19],
                                              "%Y-%m-%d %H:%M:%S") + timedelta(hours=8)
            else:
                timestamp = datetime.strptime(element['timestamp'].replace("T", " ")[0:19],
                                              "%Y-%m-%d %H:%M:%S") + timedelta(hours=9) - timedelta(minutes=5)
            open_price = element['open']
            high_price = element['high']
            low_price = element['low']
            close_price = element['close']
            volume = element['volume']
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
            start = 0
            while self.get_back_data(symbol=hour['symbol'], model=hour['obj'], bins='1h', start=start):
                start += 1000

        minute_symbols = self.symbols['5m']
        for minute in minute_symbols:
            start = 0
            while self.get_back_data(symbol=minute['symbol'], model=minute['obj'], bins='5m', start=start):
                start += 1000
