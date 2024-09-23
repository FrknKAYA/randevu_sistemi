from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from kullanicilar.models import Kullanici
from randevular.models import Randevu
from .forms import DukkanForm, BerberEkleForm, MusteriForm
from .models import Dukkan, Gun, Musteri
from django.db.models import Q # Arama için Q objesini import ediyoruz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Paginator'ı import et

@login_required
def dukkan_olustur(request):
    if request.method == 'POST':
        form = DukkanForm(request.POST)
        if form.is_valid():
            dukkan = form.save(commit=False)
            
            # SimpleLazyObject'i Kullanici nesnesine dönüştür
            dukkan.sahibi = Kullanici.objects.get(pk=request.user.pk)
            
            dukkan.save()  # Önce dükkanı kaydet

            # Çalışma günlerini ekle
            calisma_gunleri = form.cleaned_data['calisma_gunleri']
            for gun_ad in calisma_gunleri:
                gun, created = Gun.objects.get_or_create(ad=gun_ad)  # Gün varsa al, yoksa oluştur
                dukkan.calisma_gunleri.add(gun)  # Dükkanın çalışma günlerine ekle

            # Kullanıcının rolünü güncelle
            kullanici = request.user
            if kullanici.rol == 'MISAFIR':
                kullanici.rol = 'BERBER'
                kullanici.save()

            return redirect('dukkan_detay', dukkan_id=dukkan.id) 
    else:
        form = DukkanForm()
    return render(request, 'dukkanlar/dukkan_olustur.html', {'form': form})

@login_required
def dukkan_detay(request, dukkan_id):
    dukkan = get_object_or_404(Dukkan, pk=dukkan_id)
    context = {
        'dukkan': dukkan,
    }
    # Dükkan detaylarını şablona gönderin
    return render(request, 'dukkanlar/dukkan_detay.html', context)

@login_required
def berber_ekle(request, dukkan_id):
    dukkan = get_object_or_404(Dukkan, pk=dukkan_id)
    if request.user != dukkan.sahibi:
        return redirect('yetkisiz_erisim')  # Sadece dükkan sahibi berber ekleyebilir
    if request.method == 'POST':
        form = BerberEkleForm(request.POST)
        if form.is_valid():
            berber = form.save(commit=False)  # Berber nesnesini oluştur, ancak henüz kaydetme
            berber.save() # Önce berberi kaydet
            dukkan.berberler.add(berber) # Berber'i dükkanın berber listesine ekle
            return redirect('dukkan_detay', dukkan_id=dukkan.id)  # Dükkan detay sayfasına yönlendirin
    else:
        form = BerberEkleForm()
    return render(request, 'dukkanlar/berber_ekle.html', {'form': form, 'dukkan': dukkan})

@login_required
def dukkan_ayarlari(request, dukkan_id):
    dukkan = get_object_or_404(Dukkan, pk=dukkan_id)

    if request.user != dukkan.sahibi:
        return redirect('yetkisiz_erisim')  # Yetkisiz erişim

    if request.method == 'POST':
        form = DukkanForm(request.POST, instance=dukkan)
        if form.is_valid():
            form.save()
            return redirect('dukkan_detay', dukkan_id=dukkan.id)
    else:
        form = DukkanForm(instance=dukkan)

    context = {
        'dukkan': dukkan,
        'form': form
    }
    return render(request, 'dukkanlar/dukkan_ayarlari.html', context)

@login_required
def musteri_ekle(request):
    if request.method == 'POST':
        form = MusteriForm(request.POST)
        if form.is_valid():
            musteri = form.save(commit=False)
            musteri.save()

            # Berberin çalıştığı dükkanları müşteriye ekleyin
            for dukkan in request.user.calistigi_dukkanlar.all():
                musteri.dukkanlar.add(dukkan)
                
            return redirect('musteri_ekle')  # Müşteri listesine yönlendir
    else:
        form = MusteriForm()

    context = {'form': form}
    return render(request, 'dukkanlar/musteri_ekle.html', context)

@login_required
def musteri_ekle_form(request):
    if request.method == 'POST':
        form = MusteriForm(request.POST)
        if form.is_valid():
            musteri = form.save(commit=False)
            musteri.save()

            # Berberin çalıştığı dükkanları müşteriye ekleyin
            for dukkan in request.user.calistigi_dukkanlar.all():
                musteri.dukkanlar.add(dukkan)
                
            return JsonResponse({
                'musteri_adi': f"{musteri.ad} {musteri.soyad}", # Ad ve soyadı birleştir
                'musteri_id': musteri.id, 
                'message': 'Müşteri eklendi.'
            })  
        else:
            # Form geçerli değilse hataları HTML olarak döndür
            return render(request, 'dukkanlar/musteri_ekle_form.html', {'form': form, 'error': 'Formda hatalar var.'}) 
    else:
        form = MusteriForm()

    return render(request, 'dukkanlar/musteri_ekle_form.html', {'form': form})

@login_required
def musteri_listesi(request, dukkan_id):
    dukkan = get_object_or_404(Dukkan, pk=dukkan_id)

    if request.user != dukkan.sahibi and request.user not in dukkan.berberler.all():
        return redirect('yetkisiz_erisim')
    
    arama_sorgu = request.GET.get('q', '')
    musteriler = Musteri.objects.filter(
        Q(ad__icontains=arama_sorgu) | Q(soyad__icontains=arama_sorgu) | Q(telefon__icontains=arama_sorgu),
        dukkanlar=dukkan
    ).order_by('ad')

    musteri_sayisi = musteriler.count()
    sayfa_numarası = request.GET.get('sayfa', 1)
    sayfala = Paginator(musteriler, 10)

    try:
        sayfa = sayfala.page(int(sayfa_numarası))
    except PageNotAnInteger:
        sayfa = sayfala.page(1)
    except EmptyPage:
        sayfa = sayfala.page(sayfala.num_pages)

    context = {
        'dukkan': dukkan,
        'musteriler': sayfa,
        'arama_sorgu': arama_sorgu,
        'sayfa': sayfa,
        'musteri_sayisi': musteri_sayisi
    }
    return render(request, 'dukkanlar/musteri_listesi.html', context)


@login_required
def musteri_duzenle(request, dukkan_id, musteri_id):
    dukkan = get_object_or_404(Dukkan, pk=dukkan_id)
    musteri = get_object_or_404(Musteri, pk=musteri_id)

    if request.user != dukkan.sahibi and request.user not in dukkan.berberler.all():
        return redirect('yetkisiz_erisim')
    
    if request.method == 'POST':
        form = MusteriForm(request.POST, instance=musteri)
        if form.is_valid():
            form.save()
            return redirect('musteri_listesi', dukkan_id=dukkan_id)
    else:
        form = MusteriForm(instance=musteri)

    context = {'dukkan': dukkan, 'musteri': musteri, 'form': form}

    return render(request, 'dukkanlar/musteri_duzenle.html', context)

@login_required
def musteri_sil(request, dukkan_id, musteri_id):
    dukkan = get_object_or_404(Dukkan, pk=dukkan_id)
    musteri = get_object_or_404(Musteri, pk=musteri_id)
    
    if request.user != dukkan.sahibi:
        return redirect('yetkisiz_erisim')  # Sadece dükkan sahibi müşteriyi silebilir
    
    musteri.delete()
    return redirect('musteri_listesi', dukkan_id=dukkan_id)

@login_required
def musteri_detay(request, dukkan_id, musteri_id):
    dukkan = get_object_or_404(Dukkan, pk=dukkan_id)
    musteri = get_object_or_404(Musteri, pk=musteri_id)

    if request.user != dukkan.sahibi and request.user not in dukkan.berberler.all():
        return redirect('yetkisiz_erisim')
    
    randevular = Randevu.objects.filter(musteri=musteri).order_by('-tarih', '-saat')

    context = {
        'dukkan': dukkan,
        'musteri': musteri,
        'randevular': randevular,
    }
    return render(request, 'dukkanlar/musteri_detay.html', context)

@login_required
def berber_durum_degistir(request, berber_id):
    berber = get_object_or_404(Kullanici, pk=berber_id)
    
    # Berberin çalıştığı dükkanlardan birinin sahibi mi kontrol et
    sahip_dukkanlari = Dukkan.objects.filter(sahibi=request.user, berberler=berber)
    if not sahip_dukkanlari.exists():
        return redirect('yetkisiz_erisim')  # Eğer değilse yetkisiz erişim
    
    # Durumu değiştir
    berber.is_active = not berber.is_active
    berber.save()
    
    # İlk dükkanın detay sayfasına yönlendirin
    ilk_dukkan = sahip_dukkanlari.first()
    return redirect('dukkan_detay', dukkan_id=ilk_dukkan.id)

