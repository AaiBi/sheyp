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
    path('property_management_ad_detail/<int:property_pk>/<int:property_type_detail_pk>', views.property_management_ad_detail, name='property_management_ad_detail'),
                                                #property type details#
    path('edit_property_type_details/<int:property_pk>/<int:property_type_detail_pk>', views.edit_property_type_details, name='edit_property_type_details'),

                                                #Land#

]
