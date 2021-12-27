from django.db import models
from .base import HourData, MinuteData


class RealTimeData(models.Model):
    market = models.CharField(max_length=10)
    symbol = models.CharField(max_length=20)
    updated_time = models.DateTimeField(auto_now=True)
    close_price = models.FloatField()
    ask_price = models.FloatField()
    bid_price = models.FloatField()


class MainHourData(HourData):
    """
    XBT/USD
    """
    pass


class SubHourData(HourData):
    """
    XBT/EUR
    """
    pass


class ThirdHourData(HourData):
    """
    XBT/H22, XBT/F22, XBT/M22
    """
    pass


class MainMinuteData(MinuteData):
    """
    XBT/USD
    """
    pass


class SubMinuteData(MinuteData):
    """
    XBT/EUR
    """
    pass


class ThirdMinuteData(MinuteData):
    """
    XBT/H22, XBT/F22, XBT/M22
    """
    pass
