from django.urls import path
from real_estate import views

urlpatterns = [
    path('real_estate_home/', views.real_estate, name='real_estate'),

    #land
    path('land_project/', views.land_project, name='land_project'),
    path('land_projet_deletion/<int:land_project_pk>', views.land_projet_deletion, name='land_projet_deletion'),
    path('land_operation_part1/<int:land_project_pk>', views.land_operation_part1, name='land_operation_part1'),
    path('land_operation_part2/<int:land_project_pk>', views.land_operation_part2, name='land_operation_part2'),
    path('clone_land_operation/<int:land_project_pk>/<int:land_pk>', views.clone_land, name='clone_land'),
    path('delete_land/<int:land_project_pk>/<int:land_pk>', views.delete_land, name='delete_land'),
    path('edit_land/<int:land_project_pk>/<int:land_pk>', views.edit_land, name='edit_land'),
    path('land_ad_detail/<int:land_project_pk>/<int:land_pk>', views.land_ad_detail, name='land_ad_detail'),

    #Property Management
    path('property_management/', views.property_management, name='property_management'),
    path('property_management_part1/<int:property_pk>', views.property_management_part1, name='property_management_part1'),
    path('property_management_part2/<int:property_pk>', views.property_management_part2, name='property_management_part2'),
    path('property_management_deletion/<int:property_pk>', views.property_management_deletion, name='property_management_deletion'),
    path('property_management_ad_detail/<int:property_pk>/<int:object_pk>', views.property_management_ad_detail, name='property_management_ad_detail'),
                                                #Apartment#
    path('edit_apartment/<int:property_pk>/<int:apartment_pk>', views.edit_apartment, name='edit_apartment'),
    path('delete_apartment/<int:property_pk>/<int:apartment_pk>', views.delete_apartment, name='delete_apartment'),
    path('clone_apartment/<int:property_pk>/<int:apartment_pk>', views.clone_apartment, name='clone_apartment'),
                                                #Studio#
    path('edit_studio/<int:property_pk>/<int:studio_pk>', views.edit_studio, name='edit_studio'),
    path('delete_studio/<int:property_pk>/<int:studio_pk>', views.delete_studio, name='delete_studio'),
    path('clone_studio/<int:property_pk>/<int:studio_pk>', views.clone_studio, name='clone_studio'),
                                                #House#
    path('edit_house/<int:property_pk>/<int:house_pk>', views.edit_house, name='edit_house'),
    path('delete_house/<int:property_pk>/<int:house_pk>', views.delete_house, name='delete_house'),
    path('clone_house/<int:property_pk>/<int:house_pk>', views.clone_house, name='clone_house'),
                                                #Room#
    path('edit_room/<int:property_pk>/<int:room_pk>', views.edit_room, name='edit_room'),
    path('delete_room/<int:property_pk>/<int:room_pk>', views.delete_room, name='delete_room'),
    path('clone_room/<int:property_pk>/<int:room_pk>', views.clone_room, name='clone_room'),
                                                #Land#

]
