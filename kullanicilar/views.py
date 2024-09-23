from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from dukkanlar.forms import DukkanForm
from dukkanlar.models import Dukkan
from .forms import KullaniciKayitForm, ProfilDuzenlemeForm,CustomAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def kayit_gorunumu(request):
    if request.user.is_authenticated:
        return redirect('anasayfa')
    
    if request.method == 'POST':        
        form = KullaniciKayitForm(request.POST)
        if form.is_valid():
            kullanici = form.save()
            login(request, kullanici)
            return redirect('dukkan_olustur')  # Kullanıcıyı dükkan oluştur sayfasına yönlendirin
        else:
            # Form geçersiz, hata mesajı ekleyin
            form.add_error(None, 'Kayıt başarısız. Lütfen formdaki hataları düzeltin.')
    else:
        form = KullaniciKayitForm()
    
    return render(request, 'kullanicilar/kayit.html', {'form': form})

def giris_gorunumu(request):
    if request.user.is_authenticated:
        if request.user.rol == 'MISAFIR':
            return redirect('dukkan_olustur')
        return redirect('berber_randevu_listesi')
    
    if request.method == 'POST':    
        form = CustomAuthenticationForm(request, request.POST)    
        if form.is_valid():
            kullanici_adi = form.cleaned_data.get('username')
            parola = form.cleaned_data.get('password')
            kullanici = authenticate(username=kullanici_adi, password=parola)
            if kullanici is not None:
                login(request, kullanici)
                redirect_to = request.GET.get('next')
                if redirect_to:
                    return redirect(redirect_to)
                else:
                    if kullanici.rol == 'MISAFIR':
                        return redirect('dukkan_olustur')
                    return redirect('berber_randevu_listesi') # varsayılan yönlendirme
            else:
                # Giriş başarısız, form hata mesajını güncelle
                form.add_error(None, 'Geçersiz kullanıcı adı veya parola.')    
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'kullanicilar/giris.html', {'form': form})



@login_required
def profil(request):
    kullanici = request.user

    # Kullanıcının çalıştığı dükkanı al
    dukkan = get_object_or_404(Dukkan, berberler=kullanici) 

    if request.method == 'POST':
        profil_form = ProfilDuzenlemeForm(request.POST, instance=kullanici)        

        if profil_form.is_valid():
            profil_form.save()

        return redirect('profil') 

    else:
        profil_form = ProfilDuzenlemeForm(instance=kullanici)        

    return render(request, 'kullanicilar/profil.html', {
        'profil_form': profil_form,
        'dukkan': dukkan     
    })

def index(request):
    if request.user.is_authenticated:
        if request.user.rol == 'MISAFIR':
            return redirect('dukkan_olustur')
        return redirect('berber_randevu_listesi')
    return redirect('giris')