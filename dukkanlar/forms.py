from django import forms
from .models import Dukkan, Kullanici, Musteri

class DukkanForm(forms.ModelForm):
    class Meta:
        model = Dukkan
        fields = ['ad', 'adres', 'telefon', 'calisma_gunleri', 'acilis_saati', 'kapanis_saati']  # Yeni alanları ekleyin
        widgets = {
            'ad': forms.TextInput(attrs={'class': 'form-control'}),
            'adres': forms.TextInput(attrs={'class': 'form-control'}),
            'calisma_gunleri': forms.CheckboxSelectMultiple(),
            'telefon': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'pattern': '[0-9]+{11}',
                'title': 'Lütfen geçerli bir telefon numarası girin.',                
            }),
            'acilis_saati': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'kapanis_saati': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }


class BerberEkleForm(forms.ModelForm):
    class Meta:
        model = Kullanici
        fields = ('first_name', 'last_name', 'telefon_numarasi', 'email', 'username', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon_numarasi': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'pattern': '[0-9]+{11}',
                'title': 'Lütfen geçerli bir telefon numarası girin.',                
            }),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.rol = 'BERBER' # Yeni berberin rolünü 'BERBER' olarak ayarla
        if commit:
            user.save()
        return user
    
class MusteriForm(forms.ModelForm):
    class Meta:
        model = Musteri
        fields = ['ad', 'soyad', 'telefon', 'eposta']
        widgets={
            'ad': forms.TextInput(attrs={'class': 'form-control'}),
            'soyad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'pattern': '[0-9]+{11}',
                'title': 'Lütfen geçerli bir telefon numarası girin.',                
            }),
            'eposta': forms.EmailInput(attrs={'class': 'form-control'}),
        }