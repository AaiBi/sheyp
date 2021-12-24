from django.urls import path
from user import views


urlpatterns = [
    # Auth
    path('sign_up/', views.sign_up_user, name='sign_up_user'),
    path('login/', views.login_user, name='login_user'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_user, name='logout_user'),
    path('password/', views.user_password_change, name='user_password_change'),

    #real estate projects
    path('real_estate_projects/', views.real_estate_projects, name='real_estate_projects'),
    path('real_estate_project_detail/<int:land_project_pk>', views.project_detail, name='project_detail'),
    path('real_estate_project_modification/<int:land_project_pk>', views.real_estate_project_modification, name='real_estate_project_modification'),
    path('real_estate_project_deletion/<int:land_project_pk>', views.real_estate_project_deletion, name='real_estate_project_deletion'),
    path('real_estate_project_modification_land/<int:land_project_pk>/<int:land_pk>', views.land_modification, name='land_modification'),
    path('real_estate_project_land_deletion/<int:land_project_pk>/<int:land_pk>', views.land_deletion, name='land_deletion'),

    #properties projects
    path('property_project_detail/<int:property_pk>/<int:property_type_detail_pk>', views.property_project_detail, name='property_project_detail'),
    path('property_project_deletion/<int:property_pk>/<int:property_type_detail_pk>', views.property_project_deletion, name='property_project_deletion'),

    #properties projects tracker
    path('property_project_tracker/<int:property_pk>/<int:property_type_detail_pk>/<int:tracker_pk>', views.property_project_tracker, name='property_project_tracker'),
    path('property_tracker_offer_detail/<int:property_pk>/<int:property_type_detail_pk>/<int:tracker_pk>/<int:offer_pk>', views.property_tracker_offer_detail, name='property_tracker_offer_detail'),
    path('property_tracker_offer_payment/<int:property_pk>/<int:property_type_detail_pk>/<int:tracker_pk>/<int:offer_pk>', views.property_tracker_offer_payment, name='property_tracker_offer_payment'),

    #construction projects
    path('construction_projects/', views.construction_projects, name='construction_projects'),
    path('construction_project_detail/<int:construction_project_pk>', views.construction_project_detail, name='construction_project_detail'),
    path('edit_construction_floor/<int:construction_project_pk>/<int:construction_floor_pk>', views.edit_construction_floor, name='edit_construction_floor'),
    path('delete_construction_floor/<int:construction_project_pk>/<int:construction_floor_pk>', views.delete_construction_floor, name='delete_construction_floor'),
    path('construction_project_deletion/<int:construction_project_pk>', views.construction_project_deletion, name='construction_project_deletion'),

    #construction projects tracker
    path('construction_project_tracker/<int:construction_project_pk>/<int:tracker_pk>/', views.construction_project_tracker, name='construction_project_tracker'),
    path('construction_project_realisation_gallery/<int:construction_project_pk>/<int:tracker_pk>/', views.construction_project_realisation_gallery, name='construction_project_realisation_gallery'),

    #architecture project tracker
    path('projet_architecture_tracker/<int:construction_project_pk>/<int:tracker_pk>/', views.projet_architecture_tracker, name='projet_architecture_tracker'),

    #construction projects automatic counter
    path('construction_project_automatic_counter/<int:construction_project_pk>/<int:tracker_pk>/', views.construction_project_automatic_counter, name='construction_project_automatic_counter'),
    path('construction_project_deliveries/<int:construction_project_pk>/<int:tracker_pk>/', views.construction_project_deliveries, name='construction_project_deliveries'),
    path('construction_delivery_details/<int:construction_project_pk>/<int:tracker_pk>/<int:delivery_pk>/', views.construction_delivery_details, name='construction_delivery_details'),

    #cart
    path('cart/', views.cart, name='cart'),
    path('cart_payment/<int:land_pk>', views.cart_payment, name='cart_payment'),
                                        #land tracker#
    path('land_project_tracker/<int:land_project_pk>', views.land_project_tracker, name='land_project_tracker'),
    path('land_tracker_offer_detail/<int:land_project_pk>/<int:land_project_tracker_pk>/<int:offer_pk>', views.land_tracker_offer_detail, name='land_tracker_offer_detail'),
    path('land_tracker_offer_payment/<int:land_project_pk>/<int:land_project_tracker_pk>/<int:offer_pk>', views.land_tracker_offer_payment, name='land_tracker_offer_payment'),


          #########################################ADMIN PAGE##########################################################
    ###Real estate###
    path('real_estate_admin/', views.real_estate_admin, name='real_estate_admin'),
    path('real_estate_project_list/', views.real_estate_project_list, name='real_estate_project_list'),
                                                ###land####
    path('land_project_detail/<int:land_project_pk>', views.land_project_detail, name='land_project_detail'),

    ###Investment###
    ###Construction###
        #########################################END ADMIN PAGE##########################################################
]