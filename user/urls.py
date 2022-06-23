from django.urls import path
from user import views


urlpatterns = [
    # Auth
    path('sign_up/', views.sign_up_user, name='sign_up_user'),
    path('login/', views.login_user, name='login_user'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_user, name='logout_user'),
    path('password/', views.user_password_change, name='user_password_change'),

    #construction projects
    path('construction_projects/', views.construction_projects, name='construction_projects'),
    path('construction_project_detail/<int:construction_project_pk>', views.construction_project_detail, name='construction_project_detail'),
    #path('edit_construction_floor/<int:construction_project_pk>/<int:construction_floor_pk>', views.edit_construction_floor, name='edit_construction_floor'),
    path('delete_construction_floor/<int:construction_project_pk>/<int:construction_floor_pk>', views.delete_construction_floor, name='delete_construction_floor'),
    path('construction_project_deletion/<int:construction_project_pk>', views.construction_project_deletion, name='construction_project_deletion'),

    #construction projects tracker
    path('construction_project_tracker/<int:construction_project_pk>/<int:tracker_pk>/', views.construction_project_tracker, name='construction_project_tracker'),
    path('construction_project_realisation_gallery/<int:construction_project_pk>/<int:tracker_pk>/', views.construction_project_realisation_gallery, name='construction_project_realisation_gallery'),

    #construction projects automatic counter
    path('construction_project_automatic_counter/<int:construction_project_pk>/<int:tracker_pk>/', views.construction_project_automatic_counter, name='construction_project_automatic_counter'),
    path('construction_project_deliveries/<int:construction_project_pk>/<int:tracker_pk>/', views.construction_project_deliveries, name='construction_project_deliveries'),
    path('construction_delivery_details/<int:construction_project_pk>/<int:tracker_pk>/<int:delivery_pk>/', views.construction_delivery_details, name='construction_delivery_details'),

          #########################################ADMIN PAGE##########################################################


    ###Investment###
    ###Construction###
        #########################################END ADMIN PAGE##########################################################
]