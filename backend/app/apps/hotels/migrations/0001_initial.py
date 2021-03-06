# Generated by Django 3.0.3 on 2020-03-04 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.CharField(db_index=True, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('street_address', models.CharField(blank=True, max_length=200, null=True)),
                ('extended_address', models.CharField(blank=True, max_length=200, null=True)),
                ('locality', models.CharField(max_length=20, null=True)),
                ('postal_code', models.IntegerField(blank=True, db_index=True, null=True)),
                ('region', models.CharField(max_length=20, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
