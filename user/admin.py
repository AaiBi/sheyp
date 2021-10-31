from django.contrib import admin

from user.models import Customer, Cart, Cart_Payment, Land_Projet_Tracker, Land_Projet_Tracker_Offer, \
    Land_Projet_Tracker_Offer_Image, Land_Projet_Tracker_Offer_Payment, Land_Projet_Tracker_Payment_Image, \
    Delivery_Payment, Construction_Delivery_Image, \
    Construction_Delivery, Construction_Tracker_Realisation_Image, Construction_Tracker_Realisation, \
    Construction_Tracker_Sub_Step, Step_Payment, Construction_Tracker_Step, Construction_Expense, Construction_Projet_Tracker

admin.site.register(Customer)


admin.site.register(Cart)
admin.site.register(Cart_Payment)

admin.site.register(Land_Projet_Tracker)
admin.site.register(Land_Projet_Tracker_Offer)
admin.site.register(Land_Projet_Tracker_Offer_Image)
admin.site.register(Land_Projet_Tracker_Offer_Payment)
admin.site.register(Land_Projet_Tracker_Payment_Image)

admin.site.register(Construction_Projet_Tracker)
admin.site.register(Construction_Expense)
admin.site.register(Construction_Tracker_Step)
admin.site.register(Step_Payment)
admin.site.register(Construction_Tracker_Sub_Step)
admin.site.register(Construction_Tracker_Realisation)
admin.site.register(Construction_Tracker_Realisation_Image)
admin.site.register(Construction_Delivery)
admin.site.register(Delivery_Payment)
admin.site.register(Construction_Delivery_Image)