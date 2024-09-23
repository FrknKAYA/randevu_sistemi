from django.contrib import admin
from .models import Dukkan, Gun, Musteri

class DukkanAdmin(admin.ModelAdmin):
    list_display = ('ad', 'sahibi', 'adres', 'telefon')
    list_filter = ('sahibi',)  # Dükkan sahibine göre filtreleme
    filter_horizontal = ('berberler','calisma_gunleri',) # ManyToManyField için yatay filtre
    

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(sahibi=request.user)
    
class MusteriAdmin(admin.ModelAdmin):
    list_display = ('tam_ad', 'telefon', 'eposta', 'dukkan_listesi') # 'tam_ad' eklendi
    filter_horizontal = ('dukkanlar',)
    list_filter = ('dukkanlar', 'ad', 'soyad', 'telefon')
    search_fields = ('ad', 'soyad', 'telefon')  # Arama kutusu eklendi

    def dukkan_listesi(self, obj):
        return ", ".join([d.ad for d in obj.dukkanlar.all()])
    dukkan_listesi.short_description = "Kayıtlı Olduğu Dükkanlar" 

    def tam_ad(self, obj): # Yeni fonksiyon: ad ve soyadı birleştirir
        return f"{obj.ad} {obj.soyad}"
    tam_ad.short_description = "Ad Soyad" # Sütun başlığı

admin.site.register(Dukkan, DukkanAdmin)
admin.site.register(Musteri, MusteriAdmin) 
admin.site.register(Gun)