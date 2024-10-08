# Generated by Django 5.0.6 on 2024-05-11 23:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dukkanlar', '0001_initial'),
        ('kullanicilar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dukkan',
            name='sahibi',
            field=models.ForeignKey(limit_choices_to={'rol': 'DUKKAN_SAHIBI'}, on_delete=django.db.models.deletion.CASCADE, to='kullanicilar.kullanici'),
        ),
    ]
