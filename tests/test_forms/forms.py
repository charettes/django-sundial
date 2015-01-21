from __future__ import unicode_literals

from django import forms

from .models import TimezoneModel


class TimezoneModelForm(forms.ModelForm):
    class Meta:
        model = TimezoneModel
        fields = ['timezone']
