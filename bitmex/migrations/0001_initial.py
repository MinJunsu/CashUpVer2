# Generated by Django 3.2.5 on 2021-12-23 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainHourData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('time', models.CharField(max_length=20, null=True)),
                ('min_price', models.FloatField()),
                ('max_price', models.FloatField()),
                ('open_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('volume', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MainMinuteData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('time', models.CharField(max_length=20, null=True)),
                ('min_price', models.FloatField()),
                ('max_price', models.FloatField()),
                ('open_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('volume', models.IntegerField()),
                ('real', models.CharField(default='', max_length=4)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RealTimeData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(max_length=10)),
                ('symbol', models.CharField(max_length=20)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('close_price', models.FloatField()),
                ('ask_price', models.FloatField()),
                ('bid_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SubHourData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('time', models.CharField(max_length=20, null=True)),
                ('min_price', models.FloatField()),
                ('max_price', models.FloatField()),
                ('open_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('volume', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubMinuteData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('time', models.CharField(max_length=20, null=True)),
                ('min_price', models.FloatField()),
                ('max_price', models.FloatField()),
                ('open_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('volume', models.IntegerField()),
                ('real', models.CharField(default='', max_length=4)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ThirdHourData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('time', models.CharField(max_length=20, null=True)),
                ('min_price', models.FloatField()),
                ('max_price', models.FloatField()),
                ('open_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('volume', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ThirdMinuteData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('time', models.CharField(max_length=20, null=True)),
                ('min_price', models.FloatField()),
                ('max_price', models.FloatField()),
                ('open_price', models.FloatField()),
                ('close_price', models.FloatField()),
                ('volume', models.IntegerField()),
                ('real', models.CharField(default='', max_length=4)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
