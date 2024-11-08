from django.urls import path
from .views import SetupView, WebhookView

urlpatterns = [
    path('setup/', SetupView.as_view(), name='setup'),
    path('webhook/', WebhookView.as_view(), name='webhook')
]
