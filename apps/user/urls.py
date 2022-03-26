from django.urls import path

from .views import send_sms, confirm, LogoutView

app_name = 'user'

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('send_sms/', send_sms, name='send-sms'),
    path('confirm/', confirm, name='confirm'),
]
