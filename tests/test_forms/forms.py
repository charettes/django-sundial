from django import forms

from .models import TimezoneModel


class TimezoneFieldModelForm(forms.ModelForm):
    class Meta:
        model = TimezoneModel
        fields = ['timezone']


class TimezoneChoiceFieldModelForm(forms.ModelForm):
    class Meta:
        model = TimezoneModel
        fields = ['choices_timezone']
