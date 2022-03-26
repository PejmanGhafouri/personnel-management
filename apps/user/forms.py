from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from django.utils.translation import gettext as _

User = get_user_model()


class SendSmsForm(forms.Form):
    national_id = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': _('1234567890')}))

    def clean(self):
        cleaned_data = super().clean()
        national_id = cleaned_data['national_id']
        try:
            user = User.objects.get(national_id=national_id)
        except User.DoesNotExist:
            raise ValidationError(_('User is not exist!'))
        cleaned_data['phone_number'] = user.phone_number
        return cleaned_data


class ConfirmForm(forms.Form):
    confirm_code = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': _('123456')}))
