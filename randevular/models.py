from django.db import models
from kullanicilar.models import Kullanici
from dukkanlar.models import Dukkan, Musteri

class Randevu(models.Model):
    musteri = models.ForeignKey(Musteri, on_delete=models.CASCADE)
    berber = models.ForeignKey(Kullanici, on_delete=models.CASCADE, limit_choices_to={'rol': 'BERBER'})
    dukkan = models.ForeignKey(Dukkan, on_delete=models.CASCADE)
    tarih = models.DateField()
    saat = models.TimeField()

    def __str__(self):
        return f"{self.musteri} - {self.berber} - {self.tarih} {self.saat}"