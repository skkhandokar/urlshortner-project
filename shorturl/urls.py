from django.urls import path
from .views import URLShortenerView, URLRedirectView

urlpatterns = [
    path('shorten/', URLShortenerView.as_view(), name='home'),  # Home page to create short URLs
    path('<str:short_url>/', URLRedirectView.as_view(), name='redirect'),  # Redirection based on short URL
]
