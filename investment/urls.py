from django.urls import path
from investment import views


urlpatterns = [
    path('', views.investment, name='investment')
]