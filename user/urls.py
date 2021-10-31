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

    #construction projects
    path('construction_projects/', views.construction_projects, name='construction_projects'),
    path('construction_project_detail/<int:construction_project_pk>', views.construction_project_detail, name='construction_project_detail'),
    path('edit_construction_floor/<int:construction_project_pk>/<int:construction_floor_pk>', views.edit_construction_floor, name='edit_construction_floor'),
    path('delete_construction_floor/<int:construction_project_pk>/<int:construction_floor_pk>', views.delete_construction_floor, name='delete_construction_floor'),
    path('construction_project_deletion/<int:construction_project_pk>', views.construction_project_deletion, name='construction_project_deletion'),

    #construction projects tracker
    path('construction_project_tracker/<int:construction_project_pk>/<int:tracker_pk>/', views.construction_project_tracker, name='construction_project_tracker'),
    path('construction_project_realisation_gallery/<int:construction_project_pk>/<int:tracker_pk>/', views.construction_project_realisation_gallery, name='construction_project_realisation_gallery'),

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
                                        #land tracker end#
    # path('real_estate_project_detail/<int:property_pk>', views.real_estate_project_detail, name='real_estate_project_detail'),
    # path('project_update/<int:property_pk>', views.property_modification, name='property_modification'),
    # path('project_update_apartment/<int:apartment_pk>', views.apartment_info_modification, name='apartment_info_modification'),
    # path('delete_apartment/<int:apartment_pk>/<int:property_pk>', views.delete_apartment, name='delete_apartment'),
    # path('new_apartment/<int:property_pk>', views.new_apartment, name='new_apartment'),
]