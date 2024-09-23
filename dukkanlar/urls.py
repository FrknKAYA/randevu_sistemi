from django.urls import path
from . import views

urlpatterns = [
    path('olustur/', views.dukkan_olustur, name='dukkan_olustur'),
    path('<int:dukkan_id>/', views.dukkan_detay, name='dukkan_detay'),
    path('<int:dukkan_id>/ayarlar/', views.dukkan_ayarlari, name='dukkan_ayarlari'),
    path('<int:dukkan_id>/berber-ekle/', views.berber_ekle, name='berber_ekle'),
    path('musteri-ekle/', views.musteri_ekle, name='musteri_ekle'),
    path('musteri-ekle-form/', views.musteri_ekle_form, name='musteri_ekle_form'),
    path('musteri-listesi/', views.musteri_listesi, name='musteri_listesi'),
    path('<int:dukkan_id>/musteriler/', views.musteri_listesi, name='musteri_listesi'),
    path('<int:dukkan_id>/musteriler/<int:musteri_id>/', views.musteri_detay, name='musteri_detay'),
    path('<int:dukkan_id>/musteriler/<int:musteri_id>/duzenle/', views.musteri_duzenle, name='musteri_duzenle'),
    path('<int:dukkan_id>/musteriler/<int:musteri_id>/sil/', views.musteri_sil, name='musteri_sil'),
    path('berber_durum_degistir/<int:berber_id>/', views.berber_durum_degistir, name='berber_durum_degistir'),
]