from django.core.management.base import BaseCommand

from functions.collect_candle_data import BitmexBackData


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        collector = BitmexBackData()
        collector.run()
