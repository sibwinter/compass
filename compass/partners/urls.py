from django.urls import path

from . import views

app_name = 'partners'

urlpatterns = [
    path('partners/<int:partner_pk>/', views.partner_detail, name='partner_detail'),
    path('partners/', views.index, name='index'),
]
