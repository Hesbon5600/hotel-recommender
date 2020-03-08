# Generated by Django 3.0.3 on 2020-03-04 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0003_auto_20200304_0926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.CharField(db_index=True, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted', models.BooleanField(blank=True, default=False, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('thumbnail_url', models.CharField(blank=True, max_length=200, null=True)),
                ('locality', models.CharField(max_length=20, null=True)),
                ('total_reviews', models.IntegerField(null=True)),
                ('star_rating', models.FloatField(null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_address', to='hotels.Address')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
