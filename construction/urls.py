from django.urls import path
from construction import views


urlpatterns = [
    path('', views.construction, name='construction'),
    path('construction_part1', views.construction_part1, name='construction_part1'),
    path('construction_part2/<int:construction_project_pk>', views.construction_part2, name='construction_part2'),
    path('edit_construction_project/<int:construction_project_pk>', views.edit_construction_project, name='edit_construction_project'),
    path('delete_construction_project/<int:construction_project_pk>', views.delete_construction_project, name='delete_construction_project'),
    #path('delete_floor/<int:construction_project_pk>/<int:construction_floor_pk>', views.delete_floor, name='delete_floor'),
    path('edit_floor/<int:construction_project_pk>/<int:construction_floor_pk>', views.edit_floor, name='edit_floor'),
    path('clone_floor/<int:construction_project_pk>/<int:construction_floor_pk>', views.clone_floor, name='clone_floor'),
    path('construction_part3/<int:construction_project_pk>', views.construction_part3, name='construction_part3'),
]