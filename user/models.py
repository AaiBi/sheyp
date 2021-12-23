from django.db import models
from django.contrib.auth.models import User
from construction.models import Construction_Project
from real_estate.models import Land_Project, Lands, Property
from base_app.models import Provider


class Customer(models.Model):
    phone = models.CharField(max_length=100, blank=True, default="0")
    adress = models.CharField(max_length=300, blank=True)
    country = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='user/images/', blank=True)
    birth_date = models.DateField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Construction_Projet_Automatic_Counter(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    additional_info = models.TextField(blank=True, default="0")
    land_project = models.ForeignKey(Land_Project, on_delete=models.CASCADE, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Construction_Projet_Automatic_Counter_Image(models.Model):
    image = models.ImageField(upload_to='user/images/real_estate/construction/automatic_counter/', blank=True)
    construction_project_automatic_counter = models.ForeignKey(Construction_Projet_Automatic_Counter, on_delete=models.CASCADE, blank=True, default="")



        ########################################Land Tracker###########################################################
class Land_Projet_Tracker(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    land = models.ForeignKey(Lands, on_delete=models.CASCADE, default="")
    land_project = models.ForeignKey(Land_Project, on_delete=models.CASCADE, default="")


class Land_Projet_Tracker_Offer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=500, default="")
    phone_number = models.CharField(max_length=20, default="")
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    additional_info = models.TextField(blank=True, default="0")
    accepted = models.CharField(max_length=5, default="No") # can be Yes or No
    land_region = models.CharField(max_length=200, default="0")
    land_adress = models.CharField(max_length=200, default="0")
    land_area = models.IntegerField(default="0")
    land_price = models.CharField(max_length=100, default=0)
    land_plan_situation_id = models.IntegerField(default="0")
    land_paper_type_id = models.IntegerField(default="0")
    user_id = models.IntegerField(default=0) #we use it if the customer have an account
    land_project_tacker = models.ForeignKey(Land_Projet_Tracker, on_delete=models.CASCADE, default="")


class Land_Projet_Tracker_Offer_Image(models.Model):
    image = models.ImageField(
        upload_to='user/images/real_estate/land_project/tracker/offers/', blank=True)
    project_tracker_offer = models.ForeignKey(Land_Projet_Tracker_Offer, on_delete=models.CASCADE,
                                                         blank=True, default="")


class Land_Projet_Tracker_Offer_Payment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    additional_info = models.TextField(blank=True, default="")
    project_tracker_offer = models.ForeignKey(Land_Projet_Tracker_Offer, on_delete=models.CASCADE)


class Land_Projet_Tracker_Payment_Image(models.Model):
    image = models.ImageField(
        upload_to='user/images/real_estate/land_project/tracker/offers/payment/', blank=True)
    land_project_tracker_payment = models.ForeignKey(Land_Projet_Tracker_Offer_Payment, on_delete=models.CASCADE,
                                                         blank=True, default="")
        ######################################end Tracker###########################################################



########################################Construction Tracker###########################################################
########################################Construction Tracker###########################################################
########################################Construction Tracker###########################################################
class Construction_Projet_Tracker(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    construction_project = models.ForeignKey(Construction_Project, on_delete=models.CASCADE)


class Construction_Expense(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=500, default="")
    additonnal_info = models.TextField()
    image = models.ImageField(upload_to='user/images/construction/tracker/expenses/', blank=True)
    construction_project_tracker = models.ForeignKey(Construction_Projet_Tracker, on_delete=models.CASCADE)


class Construction_Tracker_Step(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Step_Payment(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    additonnal_info = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='user/images/construction/tracker/realisation/', blank=True, default="")
    construction_tracker_step = models.ForeignKey(Construction_Tracker_Step, on_delete=models.CASCADE)
    construction_project_tracker = models.ForeignKey(Construction_Projet_Tracker, on_delete=models.CASCADE, default="")


class Construction_Tracker_Sub_Step(models.Model):
    name = models.CharField(max_length=500)
    construction_tracker_step = models.ForeignKey(Construction_Tracker_Step, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.name


class Construction_Tracker_Realisation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    additonnal_info = models.TextField()
    realisation_percentage = models.IntegerField(default=0)
    construction_tracker_sub_step = models.ForeignKey(Construction_Tracker_Sub_Step, on_delete=models.CASCADE)
    construction_project_tracker = models.ForeignKey(Construction_Projet_Tracker, on_delete=models.CASCADE, default="")


class Construction_Tracker_Realisation_Image(models.Model):
    image = models.ImageField(upload_to='user/images/construction/tracker/realisation/', blank=True)
    construction_tracker_realisation = models.ForeignKey(Construction_Tracker_Realisation, on_delete=models.CASCADE)


class Construction_Delivery(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    additonnal_info = models.TextField()
    construction_project_tracker = models.ForeignKey(Construction_Projet_Tracker, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)


class Delivery_Payment(models.Model):
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    additonnal_info = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=500, default="")
    image = models.ImageField(upload_to='user/images/construction/tracker/deliveries/', blank=True)
    construction_delivery = models.ForeignKey(Construction_Delivery, on_delete=models.CASCADE, default="")


class Construction_Delivery_Image(models.Model):
    image = models.ImageField(upload_to='user/images/construction/tracker/deliveries/receipt/', blank=True)
    construction_delivery = models.ForeignKey(Construction_Delivery, on_delete=models.CASCADE)
########################################End Construction Tracker#######################################################
########################################End Construction Tracker#######################################################
########################################End Construction Tracker#######################################################



########################################Architectur Tracker###########################################################
########################################Architectur Tracker###########################################################
########################################Architectur Tracker###########################################################
class Architecture_Project_Tracker(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    additonnal_info = models.TextField()
    construction_project = models.ForeignKey(Construction_Project, on_delete=models.CASCADE)


class Architecture_Project_Tracker_Image(models.Model):
    image = models.ImageField(upload_to='user/images/construction/tracker/architecture/', blank=True)
    architecture_project_tracker = models.ForeignKey(Architecture_Project_Tracker, on_delete=models.CASCADE)
########################################End Architectur Tracker#######################################################
########################################End Architectur Tracker#######################################################
########################################End Architectur Tracker#######################################################


                                    ##Cart part##
class Cart(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=5, default="No")  # the statut can be 'done = Yes', or 'not done=No'
    payment_request = models.BooleanField(default=0) #can be 1=payment request sent, 0=payment request not sent
    land_id = models.IntegerField()
    property_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")


class Cart_Payment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    additionnal_info = models.TextField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default="")


class Cart_Payment_Image(models.Model):
    image = models.ImageField(upload_to='user/images/cart/cart/payment/', blank=True)
    cart_payment = models.ForeignKey(Cart_Payment, on_delete=models.CASCADE, default="")

                                    ##End cart##


########################################Property project Tracker###########################################################
########################################Property project Tracker###########################################################
########################################Property project Tracker###########################################################
class Property_Projet_Tracker(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, default="")


class Property_Projet_Tracker_Offer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=500, default="")
    phone_number = models.CharField(max_length=20, default="")
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    additional_info = models.TextField(blank=True, default="0")
    accepted = models.CharField(max_length=5, default="No") # can be Yes or No
    property_region = models.CharField(max_length=200, default="0")
    property_adress = models.CharField(max_length=200, default="0")
    property_area = models.IntegerField(default="0")
    property_price = models.CharField(max_length=100, default=0)
    property_type_id = models.IntegerField(default="0")
    user_id = models.IntegerField(default=0) #we use it if the customer have an account
    property_project_tacker = models.ForeignKey(Property_Projet_Tracker, on_delete=models.CASCADE, default="")


class Property_Projet_Tracker_Offer_Image(models.Model):
    image = models.ImageField(upload_to='user/images/real_estate/property_project/tracker/offers/', blank=True)
    property_project_tracker_offer = models.ForeignKey(Property_Projet_Tracker_Offer, on_delete=models.CASCADE,
                                                         blank=True, default="")


class Property_Projet_Tracker_Offer_Payment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    additional_info = models.TextField(blank=True, default="")
    property_project_tracker_offer = models.ForeignKey(Property_Projet_Tracker_Offer, on_delete=models.CASCADE)


class Property_Projet_Tracker_Payment_Image(models.Model):
    image = models.ImageField(
        upload_to='user/images/real_estate/property_project/tracker/offers/payment/', blank=True)
    property_project_tracker_payment = models.ForeignKey(Property_Projet_Tracker_Offer_Payment, on_delete=models.CASCADE,
                                                         blank=True, default="")
########################################End Property project Tracker#######################################################
########################################End Property project Tracker#######################################################
########################################End Property project Tracker#######################################################