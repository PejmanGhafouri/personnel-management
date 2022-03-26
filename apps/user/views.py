import string
from random import choice

from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.views.generic.base import View
from kavenegar import KavenegarAPI

from .forms import SendSmsForm, ConfirmForm

User = get_user_model()


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)

        return redirect('user:send_sms')


cache_help_text = 'login_sms_code_for'


def random_code_generator(size=6, code=string.digits):
    return ''.join(choice(code) for _ in range(size))


@require_http_methods(['GET', 'POST'])
def send_sms(request):
    if request.user.is_authenticated:
        return redirect(settings.DASHBOARD_REDIRECT_URL)

    form = SendSmsForm()
    if request.method == 'POST':
        form = SendSmsForm(request.POST)

        if form.is_valid():
            national_id = form.cleaned_data['national_id']
            request.session['national_id'] = national_id  # TODO (ehsan) check where sessions store?
            api = KavenegarAPI(settings.KAVENEGAR_KEYAPI)
            generated_code = random_code_generator(6)
            cache_key = '{}_{}'.format(cache_help_text, national_id)
            cache.set(cache_key, generated_code, 5 * 60)
            phone_number = form.cleaned_data['phone_number']
            api.sms_send(
                {
                    'sender': settings.SENDER_NUMBER,
                    'receptor': phone_number,
                    'message': generated_code,
                }
            )

            return redirect('user:confirm')

    return render(request, 'user/send_sms.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def confirm(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    form = ConfirmForm()
    if request.method == 'POST':
        confirm_form = ConfirmForm(request.POST)
        if confirm_form.is_valid():
            national_id = request.session['national_id']
            cache_key = '{}_{}'.format(cache_help_text, national_id)
            generated_code = cache.get(cache_key)
            confirm_code = confirm_form.cleaned_data['confirm_code']
            if confirm_code != generated_code:
                raise ValidationError(_('national_id or confirm code is not correct!'))
            user = User.objects.get(national_id=national_id)
            login(request, user)
            cache.delete(cache_key)

        return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'user/confirm.html', {'form': form})
