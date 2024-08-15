from django.urls import path

from . import views

app_name = 'short_url_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('/UrlShortener/<str:short_url>', views.redirect_to_original_url, name='redirect_to_original_url'),
]
