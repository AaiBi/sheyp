from django.urls import path
from real_estate import views

urlpatterns = [
    path('real_estate_home/', views.real_estate, name='real_estate'),
]
