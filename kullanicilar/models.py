from django.db import models
from django.contrib.auth.models import AbstractUser

class Kullanici(AbstractUser):  
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)    
    telefon_numarasi = models.CharField(max_length=11)
    rol = models.CharField(max_length=15, default='MISAFIR')
    is_active = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group', 
        verbose_name='groups', 
        blank=True, 
        related_name='kullanici_set' # Çakışmayı önlemek için related_name ekleyin
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions', 
        blank=True, 
        related_name='kullanici_set' # Çakışmayı önlemek için related_name ekleyin
    )

    def __str__(self):
        return self.username