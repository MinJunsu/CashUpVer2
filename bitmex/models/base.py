from django.db import models


class Data(models.Model):
    datetime = models.DateTimeField()
    time = models.CharField(max_length=20, null=True)
    min_price = models.FloatField()
    max_price = models.FloatField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.IntegerField()

    class Meta:
        abstract = True


class Description(models.Model):
    market = models.CharField(max_length=10)
    symbol = models.CharField(max_length=20)
    hour_table_name = models.CharField(max_length=30)
    minute_table_name = models.CharField(max_length=30)


class HourData(Data):
    class Meta:
        abstract = True
    """
    Bitmex Hour Data
    """


class MinuteData(Data):
    class Meta:
        abstract = True
    """
    Bitmex Minute Data
    """

    real = models.CharField(max_length=4, default='')
