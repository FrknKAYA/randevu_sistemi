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
        migrations.CreateModel(
            name='Musteri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad', models.CharField(max_length=100)),
                ('soyad', models.CharField(max_length=100)),
                ('telefon', models.CharField(max_length=15)),
                ('eposta', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Randevu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarih', models.DateField()),
                ('saat', models.TimeField()),
                ('berber', models.ForeignKey(limit_choices_to={'rol': 'BERBER'}, on_delete=django.db.models.deletion.CASCADE, to='kullanicilar.kullanici')),
                ('dukkan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dukkanlar.dukkan')),
                ('musteri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='randevular.musteri')),
            ],
        ),
    ]
