from django.urls import path
from administration import views


urlpatterns = [
    path('admin_page/', views.admin_login, name='admin_login'),
    #path('logout/', views.admin_logout, name='admin_logout'),
]
