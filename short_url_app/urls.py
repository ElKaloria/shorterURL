from django.urls import path

from . import views

app_name = 'short_url_app'

urlpatterns = [
    path('', views.form_view, name='form_view'),
    # path('list_user/', views.UserList.as_view(), name='UserList'),
    # path('list_url/<str:username>/', views.URLList.as_view(), name='URLList'),
    path('list_user/', views.UserUrlList.as_view(), name='UserList'),
    path('list_user/<str:username>/', views.UserUrlList.as_view(), name='UserUrlList'),
    path('list_url/', views.URLList.as_view(), name='URLList'),
    path('<str:short_url>/', views.redirect_to_original_url, name='redirect_to_original_url'),
]
