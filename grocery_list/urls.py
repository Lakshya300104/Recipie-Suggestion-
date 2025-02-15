from django.urls import path
from. import views

urlpatterns = [
    path('', views.index, name='index'),
    path('suggest_recipes/', views.suggest_recipes, name='suggest_recipes'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
]