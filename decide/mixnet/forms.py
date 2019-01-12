from django import forms
from .models import Valores, Asimetrico


class ValoresForm(forms.ModelForm):
    class Meta:
        model = Valores
        fields = ['p','g']


class ValorSimetrico(forms.ModelForm):
    class Meta:
        model = Asimetrico
        fields = ['p']