from django.urls import path
from . import views

app_name = 'anketler'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:soru_id>/', views.detail, name='detail'),
    path('<int:soru_id>/vote/', views.vote, name='vote'),
]