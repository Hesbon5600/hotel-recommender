# Generated by Django 3.0.3 on 2020-09-14 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0008_auto_20200310_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='views',
            field=models.IntegerField(null=True),
        ),
    ]
