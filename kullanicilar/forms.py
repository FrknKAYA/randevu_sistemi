from django import forms
from django.core.exceptions import ValidationError
from .models import Kullanici
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    

    def confirm_login_allowed(self, user):
        """
        Giriş yapmaya çalışan kullanıcının aktif olup olmadığını kontrol eder.
        Eğer kullanıcı aktif değilse, özel bir hata mesajı döndürür.
        """
        if not user.is_active:
            raise forms.ValidationError(
                "Bu hesap aktif değil.",
                code='inactive',
            )
        
    error_messages = {
        'invalid_login': 'Geçersiz kullanıcı adı veya parola.',
        'inactive': 'Bu hesap aktif değil.',
    }


class KullaniciKayitForm(forms.ModelForm):
    # Şifre doğrulama alanı ekleyin
    password2 = forms.CharField(label='Şifreyi tekrar girin', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Kullanici
        fields = ('username' ,'email', 'first_name', 'last_name', 'telefon_numarasi', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon_numarasi': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'pattern': '[0-9]+{11}',  # 10 haneli telefon numarası için desen
                'title': 'Lütfen geçerli bir telefon numarası girin (11 haneli).'
            }),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        telefon_numarasi = cleaned_data.get('telefon_numarasi')

        if Kullanici.objects.filter(email=email).exists():
            raise ValidationError("Bu e-posta adresi zaten kayıtlı.")

        if Kullanici.objects.filter(telefon_numarasi=telefon_numarasi).exists():
            raise ValidationError("Bu telefon numarası zaten kayıtlı.")

        return cleaned_data

    def clean_password2(self):
        # Şifre doğrulama kontrolü
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Şifreler eşleşmiyor.")
        return password2

    def save(self, commit=True):
        # Şifreyi kaydetmeden önce hashleyin
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class ProfilDuzenlemeForm(forms.ModelForm):
    class Meta:
        model = Kullanici
        fields = ['username','email', 'first_name', 'last_name', 'telefon_numarasi']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': True, 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon_numarasi': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'pattern': '[0-9]+{11}',  # 11 haneli telefon numarası için desen
                'title': 'Lütfen geçerli bir telefon numarası girin (11 haneli).'
            }),
        }