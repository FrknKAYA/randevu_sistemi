from django.contrib import admin
from .models import Randevu

class RandevuAdmin(admin.ModelAdmin):
    list_display = ('musteri', 'berber', 'dukkan', 'tarih', 'saat')
    list_filter = ('dukkan', 'berber', 'tarih')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.rol == 'DUKKAN_SAHIBI':
            return qs.filter(dukkan__sahibi=request.user)
        elif request.user.rol == 'BERBER':
            return qs.filter(berber=request.user)
        return qs.none()  # Diğer kullanıcı türleri için boş sorgu döndür

admin.site.register(Randevu, RandevuAdmin)