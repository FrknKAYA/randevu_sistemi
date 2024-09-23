import datetime
from django.urls import path, register_converter
from . import views

class TimeConverter:
    regex = r'[0-9]{2}:[0-9]{2}'

    def to_python(self, value):
        hour, minute = map(int, value.split(':'))
        return datetime.time(hour, minute)

    def to_url(self, value):
        return value.strftime('%H:%M')

register_converter(TimeConverter, 'time')

class DateConverter:
    regex = r'[0-9]{4}-[0-9]{2}-[0-9]{2}'

    def to_python(self, value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')

register_converter(DateConverter, 'date')

urlpatterns = [    
    path('olustur/', views.randevu_olustur, name='randevu_olustur'),
    path('olustur/<date:tarih>/<time:slot>/<int:berber_id>/', views.randevu_olustur, name='randevu_olustur_slot'),
    path('olustur/<date:tarih>/<time:slot>/', views.randevu_olustur, name='randevu_olustur_slot'),
    path('<int:randevu_id>/', views.randevu_detay, name='randevu_detay'),
    path('<int:randevu_id>/sil/', views.randevu_sil, name='randevu_sil'),
    path('dukkan/<int:dukkan_id>/', views.dukkan_randevu_listesi, name='dukkan_randevu_listesi'),
    path('<int:yil>/<int:ay>/<int:gun>/<int:berber_id>/', views.berber_randevu_listesi, name='berber_randevu_listesi_tarih'),
    path('berber/', views.berber_randevu_listesi, name='berber_randevu_listesi'),
    path('berber/<int:berber_id>/randevular/', views.berber_randevulari, name='berber_randevulari'),
    path('musteri/<int:dukkan_id>/', views.musteri_randevu_listesi, name='musteri_randevu_listesi'),
]