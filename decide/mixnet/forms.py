from django import forms
from .models import Valores


class ValoresForm(forms.ModelForm):
    class Meta:
        model = Valores
        fields = ['p','g']