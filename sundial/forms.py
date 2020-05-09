from django.forms import CharField, TypedChoiceField
from django.utils.encoding import force_str

from .utils import coerce_timezone


class TimezoneField(CharField):
    def to_python(self, value):
        if value in self.empty_values:
            return ''
        return coerce_timezone(value)

    def run_validators(self, value):
        return super().run_validators(force_str(value))


class TimezoneChoiceField(TypedChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('coerce', coerce_timezone)
        super().__init__(*args, **kwargs)
