from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('kayit/', views.kayit_gorunumu, name='kayit'),
    path('giris/', views.giris_gorunumu, name='giris'),
    path('profil/', views.profil, name='profil'),
    path('cikis/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]