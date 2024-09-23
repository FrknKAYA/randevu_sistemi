import datetime
from django.db import models
from kullanicilar.models import Kullanici

class Gun(models.Model):
    ad = models.CharField(max_length=255)

    def __str__(self):
        return self.ad

class GUNLER(models.TextChoices):
    MONDAY = 'MONDAY', 'Pazartesi'  
    TUESDAY = 'TUESDAY', 'Salı'
    WEDNESDAY = 'WEDNESDAY', 'Çarşamba'
    THURSDAY = 'THURSDAY', 'Perşembe'
    FRIDAY = 'FRIDAY', 'Cuma'
    SATURDAY = 'SATURDAY', 'Cumartesi'
    SUNDAY = 'SUNDAY', 'Pazar' 

class Dukkan(models.Model):
    ad = models.CharField(max_length=255)
    adres = models.CharField(max_length=255)
    telefon = models.CharField(max_length=11)
    sahibi = models.ForeignKey(Kullanici, on_delete=models.CASCADE, related_name='dukkanlar')
    berberler = models.ManyToManyField(Kullanici, related_name='calistigi_dukkanlar', blank=True)

    calisma_gunleri = models.ManyToManyField(Gun, related_name='dukkanlar', blank=True)  # ManyToManyField ile Gün modeline bağladık
    acilis_saati = models.TimeField(default=datetime.time(9, 30))
    kapanis_saati = models.TimeField(default=datetime.time(21, 0))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pk and self.sahibi not in self.berberler.all():
            self.berberler.add(self.sahibi)
            
    def __str__(self):
        return self.ad

class Musteri(models.Model):
    ad = models.CharField(max_length=100, db_index=True)
    soyad = models.CharField(max_length=100)
    telefon = models.CharField(max_length=11, blank=True, null=True, db_index=True)
    eposta = models.EmailField(blank=True)  # E-posta isteğe bağlı olabilir
    dukkanlar = models.ManyToManyField(Dukkan, related_name='musteriler', blank=True)

    def __str__(self):
        return f"{self.ad} {self.soyad}"