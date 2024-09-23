from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Kullanici

class KullaniciAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'telefon_numarasi', 'rol', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Ek Bilgiler', {'fields': ('telefon_numarasi', 'rol')}),
    )

admin.site.register(Kullanici, KullaniciAdmin)