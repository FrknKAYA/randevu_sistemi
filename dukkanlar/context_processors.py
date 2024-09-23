from .models import Dukkan

def dukkan_bilgisi(request):
    dukkan = None
    if request.user.is_authenticated:
        try:
            dukkan = request.user.calistigi_dukkanlar.first()
        except Dukkan.DoesNotExist:
            print("Kullanıcının çalıştığı bir dükkan bulunamadı!")
    return {'dukkan': dukkan}