from datetime import datetime, date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from kullanicilar.models import Kullanici
from .forms import RandevuForm
from .models import Randevu, Dukkan

@login_required
def randevu_olustur(request, tarih=None, slot=None, berber_id=None):
    # Tarihi ve slot'u string'den date ve time objelerine dönüştür
    if tarih:
        tarih_str_yeni = tarih.strftime("%Y-%m-%d")
    else:
        tarih_str_yeni = date.today().strftime('%Y-%m-%d')

    if request.method == 'POST':
        # POST isteğinde gelen tarih bilgisini de forma ekle
        request.POST = request.POST.copy() # ImmutableQueryDict olduğu için kopyalıyoruz
        #request.POST['tarih'] = tarih_str_yeni

        randevu_form = RandevuForm(request.user.calistigi_dukkanlar.first(), request.POST)
        if randevu_form.is_valid():
            randevu = randevu_form.save()
            return redirect('randevu_detay', randevu_id=randevu.id)
        else:
            for error in randevu_form.errors:
                messages.error(request, randevu_form.errors[error])
    else:
        dukkan = request.user.calistigi_dukkanlar.first()

        # Eğer URL'de berber_id varsa, o berberi al, yoksa geçerli kullanıcıyı kullan
        if berber_id:
            berber = get_object_or_404(Kullanici, pk=berber_id)
        else:
            berber = request.user
        
        initial = {'saat': slot, 'tarih': tarih_str_yeni, 'berber': berber} if slot else {'berber': berber}
        randevu_form = RandevuForm(dukkan, initial=initial)

    context = {
        'randevu_form': randevu_form,
    }
    return render(request, 'randevular/randevu_olustur.html', context)

@login_required
def dukkan_randevu_listesi(request, dukkan_id):
    dukkan = get_object_or_404(Dukkan, pk=dukkan_id)
    simdi = datetime.now()
    bir_saat_oncesi = simdi - timedelta(hours=1)

    randevular = Randevu.objects.filter(
        dukkan=dukkan,
        tarih=simdi.date(),  # Sadece bugünün randevularını al
        saat__gte=bir_saat_oncesi.time()  # Bir saat öncesi ve sonrasındaki randevuları al
    ).order_by('saat')
    return render(request, 'randevular/dukkan_randevu_listesi.html', {'dukkan': dukkan, 'randevular': randevular})

@login_required
def randevu_detay(request, randevu_id):
    randevu = get_object_or_404(Randevu, pk=randevu_id)
    # Randevu detaylarını şablona gönderin
    return render(request, 'randevular/randevu_detay.html', {'randevu': randevu})

@login_required
def randevu_sil(request, randevu_id):
    randevu = get_object_or_404(Randevu, pk=randevu_id)
    
    # Randevunun berbere ait olduğunu doğrulayın
    if randevu.berber != request.user:
        return redirect('yetkisiz_erisim')
    
    randevu.delete()
    messages.success(request, 'Randevu başarıyla silindi.')  
    return redirect('berber_randevu_listesi')

def randevu_slotlari_olustur(randevular, tarih, acilis_saati, kapanis_saati): # Tarih argümanını ekledik
    baslangic_saati = acilis_saati
    bitis_saati = kapanis_saati
    slotlar = []
    
    while baslangic_saati < bitis_saati:
        slot = {
            'saat': baslangic_saati,
            'durum': 'Boş'  # Başlangıçta tüm slotlar boş
        }

        # Slot saatine ait bir randevu var mı kontrol et
        for randevu in randevular:
            if randevu.saat == slot['saat'] and randevu.tarih == tarih:  # Tarih kontrolünü güncelledik
                slot['durum'] = {'musteri_adi': f'{randevu.musteri}', 'randevu_id': randevu.id}  # randevu.id'yi ekledik
                break

        slotlar.append(slot)
        baslangic_saati = (datetime.combine(date.today(), baslangic_saati) + timedelta(minutes=30)).time()

    return slotlar

@login_required
def berber_randevu_listesi(request, yil=None, ay=None, gun=None, berber_id=None):
    if request.user.rol == 'BERBER':
        # Tarih bilgisi yoksa bugünün tarihini al
        try:
            bugun = date(int(yil), int(ay), int(gun))
        except (TypeError, ValueError):
            bugun = date.today()

        # Dükkandan açılış ve kapanış saatini al
        dukkan = request.user.calistigi_dukkanlar.first()
        acilis_saati = dukkan.acilis_saati
        kapanis_saati = dukkan.kapanis_saati

        randevular = Randevu.objects.filter(berber=request.user, tarih=bugun)
        randevu_slotlari = randevu_slotlari_olustur(randevular, bugun, acilis_saati, kapanis_saati)

        # Çalışma günlerini sayısal değerlere dönüştür
        calisma_gunleri = [
            0 if gun == "Pazartesi" else 1 if gun == "Salı" else 2 if gun == "Çarşamba" else 3 if gun == "Perşembe" else 4 if gun == "Cuma" else 5 if gun == "Cumartesi" else 6
            for gun in request.user.calistigi_dukkanlar.first().calisma_gunleri.values_list('ad', flat=True)
        ]

        # İleri ve geri butonları için tarihler
        onceki_gun = bugun - timedelta(days=1)
        sonraki_gun = bugun + timedelta(days=1)

        context = {
            'randevular': randevular,
            'randevu_slotlari': randevu_slotlari,
            'bugun': bugun,
            'onceki_gun': onceki_gun,
            'sonraki_gun': sonraki_gun,
            'calisma_gunleri': calisma_gunleri,
        }

        return render(request, 'randevular/berber_randevu_listesi.html', context)
    else:
        return redirect('yetkisiz_erisim')

@login_required
def musteri_randevu_listesi(request, dukkan_id):
    dukkan = get_object_or_404(Dukkan, pk=dukkan_id)
    # Dükkanın tüm randevularını (tüm berberler dahil) alın
    randevular = Randevu.objects.filter(dukkan=dukkan)
    return render(request, 'randevular/musteri_randevu_listesi.html', {'dukkan': dukkan, 'randevular': randevular})

@login_required
def berber_randevulari(request, berber_id):
    berber = get_object_or_404(Kullanici, pk=berber_id)
    
    #dükkan sahibi kontrolü yapılacak dükkan sahibine özel

    # Tarih bilgisi yoksa bugünün tarihini al
    yil = request.GET.get('yil')
    ay = request.GET.get('ay')
    gun = request.GET.get('gun')
    try:
        bugun = date(int(yil), int(ay), int(gun))             
    except (TypeError, ValueError): 
        bugun = date.today()

    # Dükkandan açılış ve kapanış saatini al
    dukkan = berber.calistigi_dukkanlar.first() # Berberin dükkanını alıyoruz
    acilis_saati = dukkan.acilis_saati
    kapanis_saati = dukkan.kapanis_saati

    randevular = Randevu.objects.filter(berber=berber, tarih=bugun) # Berberin randevularını alıyoruz
    randevu_slotlari = randevu_slotlari_olustur(randevular, bugun, acilis_saati, kapanis_saati)

    # Çalışma günlerini sayısal değerlere dönüştür
    calisma_gunleri = [
        0 if gun == "Pazartesi" else 1 if gun == "Salı" else 2 if gun == "Çarşamba" else 3 if gun == "Perşembe" else 4 if gun == "Cuma" else 5 if gun == "Cumartesi" else 6
        for gun in dukkan.calisma_gunleri.values_list('ad', flat=True) 
    ]
    
    # İleri ve geri butonları için tarihler
    onceki_gun = bugun - timedelta(days=1)
    sonraki_gun = bugun + timedelta(days=1)
    
    context = {
        'randevular': randevular,
        'randevu_slotlari': randevu_slotlari,
        'bugun': bugun,
        'onceki_gun': onceki_gun,
        'sonraki_gun': sonraki_gun,
        'calisma_gunleri': calisma_gunleri,
        'berber': berber,  # 'berber' değişkenini context'e ekleyin
    }

    return render(request, 'randevular/berber_randevulari.html', context)