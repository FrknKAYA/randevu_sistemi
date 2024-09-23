# Generated by Django 5.0.6 on 2024-05-15 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dukkanlar', '0005_dukkan_acilis_saati_dukkan_calisma_gunleri_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dukkan',
            name='calisma_gunleri',
            field=models.CharField(blank=True, choices=[('Pazartesi', 'Pazartesi'), ('Salı', 'Salı'), ('Çarşamba', 'Çarşamba'), ('Perşembe', 'Perşembe'), ('Cuma', 'Cuma'), ('Cumartesi', 'Cumartesi'), ('Pazar', 'Pazar')], default=['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], max_length=255),
        ),
    ]
