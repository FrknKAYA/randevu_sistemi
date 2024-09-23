from django import forms
from kullanicilar.models import Kullanici
from .models import Randevu, Musteri

class RandevuForm(forms.ModelForm):
    class Meta:
        model = Randevu
        fields = ['musteri', 'tarih', 'saat', 'dukkan', 'berber']
        widgets = {
            'musteri': forms.Select(attrs={'class': 'form-control', 'id': 'id_musteri'}),
            'tarih': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'saat': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'berber': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, dukkan, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dukkan'].widget = forms.HiddenInput()
        self.fields['dukkan'].initial = dukkan
        self.fields['musteri'].queryset = Musteri.objects.filter(dukkanlar=dukkan)
        self.fields['berber'].queryset = Kullanici.objects.filter(calistigi_dukkanlar=dukkan, rol='BERBER', is_active=True)
        self.fields['berber'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

    def clean(self):
        cleaned_data = super().clean()
        tarih = cleaned_data.get('tarih')
        saat = cleaned_data.get('saat')
        berber = cleaned_data.get('berber')

        if tarih and saat and berber:
            mevcut_randevular = Randevu.objects.filter(tarih=tarih, saat=saat, berber=berber)
            if mevcut_randevular.exists():
                raise forms.ValidationError("Bu tarih ve saatte zaten bir randevu var. Farklı bir saat deneyin!")
        
        return cleaned_data
