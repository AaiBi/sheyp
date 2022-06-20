from django.urls import path
from construction import views


urlpatterns = [
    path('', views.construction, name='construction'),
    path('automatic_quote', views.automatic_quote, name='automatic_quote'),
    path('automatic_quote_result/<int:quote_pk>', views.automatic_quote_result, name='automatic_quote_result'),

    path('construction_part1', views.construction_part1, name='construction_part1'),
    path('construction_part2/<str:client_first_name>/<str:client_last_name>/<str:client_email>/'
         '<str:client_phone_number>', views.construction_part2, name='construction_part2'),
    path('construction_part3/<int:construction_project_pk>', views.construction_part3, name='construction_part3'),
]