from datetime import date
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from base_app.models import Provider
from construction.forms import Construction_floor_Form
from construction.models import Construction_Project, Construction_Type, Construction_floor, Architecture_Image, \
    Construction_Service
from real_estate.models import Land_Project, Real_Estate_Projet_Type, Land_Type, Service_Type, Lands, Land_Images1, \
    Land_Plan_Situation, Land_Paper_Type, Property, Property_Type_Details, Property_Type_Details_Image, Property_Type
from user.forms import EditUserInfoForm, EditUserInfoForm1, EditUserPasswordForm, Land_Form, Land_Project_Form, \
    Land_Projet_Tracker_Offer_Form, Property_Projet_Tracker_Offer_Form
from user.models import Customer, Cart, Land_Projet_Tracker, Land_Projet_Tracker_Offer, Land_Projet_Tracker_Offer_Image, \
    Land_Projet_Tracker_Offer_Payment, Land_Projet_Tracker_Payment_Image, Construction_Projet_Tracker, \
    Construction_Tracker_Step, Construction_Tracker_Sub_Step, Construction_Tracker_Realisation, \
    Construction_Tracker_Realisation_Image, Construction_Expense, Step_Payment, Construction_Delivery, Delivery_Payment, \
    Construction_Delivery_Image, Property_Projet_Tracker, Property_Projet_Tracker_Offer, \
    Property_Projet_Tracker_Offer_Image, Property_Projet_Tracker_Offer_Payment, Property_Projet_Tracker_Payment_Image, \
    Architecture_Project_Tracker, Architecture_Project_Tracker_Image


def login_user(request):
    if request.method == 'GET':
        return render(request, 'user/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'user/login_user.html', {'form': AuthenticationForm(), 'error': 'Votre nom d\'utilisateur et mot de passe ne correspondent pas !'})
        else:
            login(request, user)
            return redirect('profile')


def sign_up_user(request):
    if request.method == 'GET':
        return render(request, 'user/sign_up_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password'] == request.POST['password1']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'],
                                                first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                                                email=request.POST['email'])

                #creating the blanck customer table
                user_id  = user.id
                phone = 0
                adress = ""
                country = ""
                birth_date = date.today()
                customer_info = Customer(phone=phone, adress=adress, country=country, birth_date=birth_date,
                                         user_id=user_id)
                customer_info.save()
                user.save()

                messages.success(request, f'Bienvenue chez Sheyp Mr/Mme {user.last_name}, votre compte a été créer !')
                return redirect('login_user')
            except ValueError:
                return render(request, 'user/sign_up_user.html', {'form': UserCreationForm(), 'error': 'Bad data passed in'})
        else:
            return render(request, 'user/sign_up_user.html', {'form': UserCreationForm(), 'error': 'Les deux mots de passe ne correspondent pas !'})


@login_required
def profile(request):
    customer_info = get_object_or_404(Customer, user=request.user)
    customer_profile_verification = Customer.objects.filter(user=request.user)
    form = EditUserInfoForm(instance=request.user)
    form1 = EditUserInfoForm1(instance=request.user)

    # datas from the first form
    if 'save_form' in request.POST:
        if request.method == 'POST':
            form = EditUserInfoForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Vos informations ont été modifiées !')
                return redirect('profile')
        else:
            form = EditUserInfoForm(instance=request.user)

    # datas from the second form
    if 'save_form1' in request.POST:
        if request.method == 'GET':
            form1 = EditUserInfoForm1(instance=customer_info)
            return render(request, 'user/profile/profile.html', {'customer_info': customer_info, 'customer_profile_verification': customer_profile_verification, 'form1': form1})
        else:
            try:
                form1 = EditUserInfoForm1(request.POST, instance=customer_info)
                if request.POST.get('phone').isnumeric():
                    if form1.is_valid():
                        form1.save()
                        messages.success(request, 'Vos informations ont été modifiées !')
                        return redirect('profile')
                else:
                    messages.error(request, 'Le numéro de téléphone ne doit contenir que des chiffres !')
            except ValueError:
                return render(request, 'user/profile/profile.html', {'customer_info': customer_info, 'customer_profile_verification': customer_profile_verification, 'form1': form1
                , 'error': 'Mauvaises données saisies !'})

    return render(request, 'user/profile/profile.html', {'customer_info': customer_info, 'customer_profile_verification': customer_profile_verification, 'form': form, 'form1': form1})


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login_user')


@login_required
def user_password_change(request):
    if request.method == 'POST':
        form = EditUserPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Votre mot de passe a été modifié avec succès !')
            return redirect('profile')
    else:
        form = EditUserPasswordForm(request.user)
    return render(request, 'user/profile/user_password_change.html', {'form': form})


######################################real estat projects#########################################
@login_required
def real_estate_projects(request):
    land_projects = Land_Project.objects.filter(user=request.user).order_by('-created')
    real_estate_projects_type = Real_Estate_Projet_Type.objects.all()
    land_types = Land_Type.objects.all()
    service_types = Service_Type.objects.all()
    properties = Property.objects.filter(user=request.user).order_by('-created')
    property_type_details = Property_Type_Details.objects.all()
    property_type_details_images = Property_Type_Details_Image.objects.all()
    property_types = Property_Type.objects.all()

    return render(request, 'user/real_estate_projects/real_estate_projects.html', {
        'land_projects': land_projects, 'real_estate_projects_type': real_estate_projects_type, 'land_types':
         land_types, 'service_types': service_types, 'properties': properties, 'property_type_details': property_type_details,
        'property_type_details_images': property_type_details_images, 'property_types': property_types})



@login_required
def real_estate_project_modification(request, land_project_pk):
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    real_estate_projects_type = Real_Estate_Projet_Type.objects.all()
    land_types = Land_Type.objects.all()
    land_plan_situations = Land_Plan_Situation.objects.all()
    service_types = Service_Type.objects.all()
    lands = Lands.objects.filter(land_project_id=land_project_pk)
    images = Land_Images1.objects.all()

    if request.method == 'GET':
        form = Land_Project_Form(instance=land_project)
        return render(request, 'user/real_estate_projects/real_estate_project_modification.html', {'land_project': land_project,
                                                                             'real_estate_projects_type':
                                                                                 real_estate_projects_type,
                                                                             'land_types':
                                                                                 land_types, 'lands': lands, 'images':
                                                                                 images, 'form': form,
                                                                             'land_plan_situations': land_plan_situations,
                                                                             'service_types': service_types})
    else:
        try:
            form = Land_Project_Form(request.POST, instance=land_project)
            form = form.save(commit=False)
            form.real_estate_project_type = get_object_or_404(Real_Estate_Projet_Type,
                                                         id=request.POST.get('real_estate_project_type_id'))
            form.land_project = get_object_or_404(Land_Project, id=land_project_pk)
            form.service_type = get_object_or_404(Service_Type, id=request.POST.get('service_type_id'))
            form.save()
            messages.success(request, 'Modification éffectuée !')
            return redirect('real_estate_projects')
        except ValueError:
            return render(request, 'user/real_estate_projects/real_estate_project_modification.html', {'land_project':
                                                                                                           land_project,
                                                                             'real_estate_projects_type':
                                                                                 real_estate_projects_type,
                                                                             'land_types':
                                                                                 land_types, 'lands': lands, 'images':
                                                                                 images, 'form': form,
                                                                             'land_plan_situations': land_plan_situations,
                                                                             'service_types': service_types,
                                                                         'error': 'Mauvaises données saisies !'})


@login_required
def project_detail(request, land_project_pk):
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    real_estate_projects_type = Real_Estate_Projet_Type.objects.all()
    land_types = Land_Type.objects.all()
    land_plan_situations = Land_Plan_Situation.objects.all()
    service_types = Service_Type.objects.all()
    lands = Lands.objects.filter(land_project_id=land_project_pk)
    images = Land_Images1.objects.all()

    land_project_tracker = Land_Projet_Tracker.objects.all()
    # land_project_tracker = Land_Projet_Tracker.objects.filter(land_project_id=land_project_pk)
    # land_project_tracker_offer = Land_Projet_Tracker_Offer.objects.all()
    # land_project_tracker_offer_achat = Land_Projet_Tracker_Offer_Achat.objects.all().order_by('-id')
    # land_project_tracker_offer_response_achat = Land_Projet_Tracker_Offer_Achat_Response.objects.all()
    return render(request, 'user/real_estate_projects/project_detail.html',
                  {'land_project': land_project, 'real_estate_projects_type': real_estate_projects_type,
                   'land_types':
                    land_types, 'lands': lands, 'images': images, 'land_plan_situations': land_plan_situations,
                    'service_types': service_types})


@login_required
def real_estate_project_deletion(request, land_project_pk):
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    service_types = Service_Type.objects.all()
    real_estate_projects_type = Real_Estate_Projet_Type.objects.all()
    land_types = Land_Type.objects.all()

    if request.method == 'GET':
        return render(request, 'user/real_estate_projects/real_estate_project_deletion.html',
                      {'land_project':
                        land_project, 'service_types': service_types, 'land_types': land_types,
                        'real_estate_projects_type': real_estate_projects_type})
    if request.method == 'POST':
        land_project.delete()
        messages.success(request, 'Suppression effectuée !')
        return redirect('real_estate_projects')


@login_required
def land_modification(request, land_project_pk, land_pk):
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    land_info = get_object_or_404(Lands, pk=land_pk)
    land_plan_situations = Land_Plan_Situation.objects.all()
    images = Land_Images1.objects.filter(land_id=land_pk)
    service_type_vente = Service_Type.objects.filter(name="Vente")  # sale

    if request.method == 'GET':
        form = Land_Form(instance=land_info)
        return render(request, 'user/real_estate_projects/land_modification.html', {'land_info': land_info, 'form': form, 'land_project':
                                                                    land_project, 'land_plan_situations': land_plan_situations,
                                                                       'images': images, 'service_type_vente':
                                                                                    service_type_vente})
    else:
        try:
            form = Land_Form(request.POST, instance=land_info)
            form = form.save(commit=False)
            form.land_plan_situation = get_object_or_404(Land_Plan_Situation,
                                                         id=request.POST.get('land_plan_situation_id'))
            form.land_project = get_object_or_404(Land_Project, id=land_project_pk)
            form.save()
            messages.success(request, 'Modification éffectuée !')
            return redirect('project_detail', land_project_pk=land_project_pk)
        except ValueError:
            return render(request, 'user/real_estate_projects/land_modification.html', {'land_info': land_info, 'form': form, 'land_project':
                                                                    land_project, 'land_plan_situations': land_plan_situations,
                                                                       'images': images, 'service_type_vente': service_type_vente,
                                                                         'error': 'Mauvaises données saisies !'})


@login_required
def land_deletion(request, land_project_pk, land_pk):
    land = get_object_or_404(Lands, pk=land_pk)
    lands = Lands.objects.filter(land_project_id=land_project_pk)
    land_types = Land_Type.objects.filter()
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    service_types = Service_Type.objects.all()
    service_type_vente = Service_Type.objects.filter(name="Vente")  # sale
    land_plan_situation = Land_Plan_Situation.objects.all()

    if request.method == 'GET':
        return render(request, 'user/real_estate_projects/land_deletion.html',
                      {'land': land, 'land_project':
                        land_project, 'land_types': land_types,
                        'lands': lands,
                        'service_types':
                        service_types, 'land_plan_situation':
                        land_plan_situation, 'service_type_vente':
                        service_type_vente, 'land_project_pk': land_project_pk})
    if request.method == 'POST':
        land.delete()
        messages.success(request, 'Suppression effectuée !')
        return redirect('project_detail', land_project_pk=land_project_pk)



###################################################PROPERTY PROJECT#############################################
###################################################PROPERTY PROJECT#############################################
###################################################PROPERTY PROJECT#############################################
@login_required
def property_project_detail(request, property_pk, property_type_detail_pk):
    property_project = get_object_or_404(Property, pk=property_pk, user=request.user)
    property_types = Property_Type.objects.all()
    property_type_detail = get_object_or_404(Property_Type_Details, pk=property_type_detail_pk)
    property_type_detail_images = Property_Type_Details_Image.objects.all()
    service_types = Service_Type.objects.all()
    property_project_trackers = Property_Projet_Tracker.objects.filter(property_id=property_pk)

    return render(request, 'user/real_estate_projects/properties/property_project_detail.html',
                  {'property_project': property_project, 'property_types': property_types, 'property_type_detail':
                      property_type_detail, 'property_type_detail_images': property_type_detail_images, 'service_types':
                   service_types, 'property_project_trackers': property_project_trackers})


@login_required
def property_project_deletion(request, property_pk, property_type_detail_pk):
    property_project = get_object_or_404(Property, pk=property_pk, user=request.user)
    property_types = Property_Type.objects.all()
    property_type_detail = get_object_or_404(Property_Type_Details, pk=property_type_detail_pk)
    property_type_detail_images = Property_Type_Details_Image.objects.all()
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        return render(request, 'user/real_estate_projects/properties/property_project_deletion.html',
                      {'property_project': property_project, 'property_types': property_types, 'property_type_detail':
                      property_type_detail, 'property_type_detail_images': property_type_detail_images, 'service_types':
                   service_types})
    if request.method == 'POST':
        property_project.delete()
        messages.success(request, 'Suppression effectuée !')
        return redirect('real_estate_projects')
###################################################END PROPERTY PROJECT#############################################
###################################################END PROPERTY PROJECT#############################################
###################################################END PROPERTY PROJECT#############################################


##############################################PROPERTY PROJECT TRACKER#############################################
##############################################PROPERTY PROJECT TRACKER#############################################
##############################################PROPERTY PROJECT TRACKER#############################################
@login_required
def property_project_tracker(request, property_pk, property_type_detail_pk, tracker_pk):
    property_project = get_object_or_404(Property, pk=property_pk, user=request.user)
    property_type_detail = get_object_or_404(Property_Type_Details, pk=property_type_detail_pk)
    property_project_tracker = get_object_or_404(Property_Projet_Tracker, pk=tracker_pk)
    property_project_tracker_offers = Property_Projet_Tracker_Offer.objects.filter(property_project_tacker_id=tracker_pk).order_by('-created')
    if request.method == 'GET':
        return render(request, 'user/real_estate_projects/property_tracker/property_project_tracker.html',
                      {'property_project': property_project, 'property_type_detail': property_type_detail,
                       ' property_project_tracker': property_project_tracker, 'property_project_tracker_offers':
                       property_project_tracker_offers, 'tracker_pk': tracker_pk})


@login_required
def property_tracker_offer_detail(request, property_pk, property_type_detail_pk, tracker_pk, offer_pk):
    property_project = get_object_or_404(Property, pk=property_pk, user=request.user)
    property_type_detail = get_object_or_404(Property_Type_Details, pk=property_type_detail_pk)
    property_project_tracker = get_object_or_404(Property_Projet_Tracker, pk=tracker_pk)
    offer = get_object_or_404(Property_Projet_Tracker_Offer, pk=offer_pk)
    offer_images = Property_Projet_Tracker_Offer_Image.objects.filter(property_project_tracker_offer_id=offer_pk)
    service_types = Service_Type.objects.all()
    property_types = Property_Type.objects.all()

    if request.method == 'GET':
        form = Property_Projet_Tracker_Offer_Form(instance=offer)
        return render(request, 'user/real_estate_projects/property_tracker/property_tracker_offer_detail.html',
                      {'property_project': property_project, 'property_project_tracker': property_project_tracker, 'form': form,
                       'offer_images': offer_images, 'tracker_pk': tracker_pk, 'offer': offer, 'service_types': service_types,
                       'property_type_detail': property_type_detail, 'property_types': property_types})
    else:
        try:
            form = Property_Projet_Tracker_Offer_Form(request.POST, instance=offer)

            if 'offer_accepted' in request.POST:
                form = form.save(commit=False)
                form.property_project_tacker = get_object_or_404(Property_Projet_Tracker,
                                                id=request.POST.get('property_project_tacker_id'))
                form.save()
                messages.success(request, 'Cette offre a été acceptée avec succès !')
                return redirect('property_project_tracker', property_pk=property_pk, property_type_detail_pk=property_type_detail_pk
                                , tracker_pk=tracker_pk)

        except ValueError:
            return render(request, 'user/real_estate_projects/property_tracker/property_tracker_offer_detail.html',
                          {'property_project': property_project, 'property_project_tracker':
                          property_project_tracker, 'form': form, 'offer_images': offer_images, 'tracker_pk': tracker_pk,
                           'property_type_detail': property_type_detail, 'offer': offer, 'service_types': service_types,
                           'error': 'Une erreur est survenue !'})


@login_required
def property_tracker_offer_payment(request, property_pk, property_type_detail_pk, tracker_pk, offer_pk):
    property_project = get_object_or_404(Property, pk=property_pk, user=request.user)
    property_type_detail = get_object_or_404(Property_Type_Details, pk=property_type_detail_pk)
    property_project_tracker = get_object_or_404(Property_Projet_Tracker, pk=tracker_pk)
    offer = get_object_or_404(Property_Projet_Tracker_Offer, pk=offer_pk)
    property_tracker_offer_payment = Property_Projet_Tracker_Offer_Payment.objects.filter(
                                    property_project_tracker_offer_id=offer_pk)
    property_tracker_offer_payment_images = Property_Projet_Tracker_Payment_Image.objects.all()
    property_types = Property_Type.objects.all()
    if request.method == 'GET':
        return render(request, 'user/real_estate_projects/property_tracker/property_tracker_offer_payment.html',
                      {'property_project': property_project, 'property_project_tracker':
                          property_project_tracker, 'tracker_pk': tracker_pk, 'property_tracker_offer_payment':
                          property_tracker_offer_payment, 'property_tracker_offer_payment_images':
                          property_tracker_offer_payment_images, 'property_types': property_types,
                           'property_type_detail': property_type_detail, 'offer': offer})
###########################################END PROPERTY PROJECT TRACKER#############################################
###########################################END PROPERTY PROJECT TRACKER#############################################
###########################################END PROPERTY PROJECT TRACKER#############################################


##############################################LAND PROJECT TRACKER#############################################
##############################################LAND PROJECT TRACKER#############################################
##############################################LAND PROJECT TRACKER#############################################
@login_required
def land_project_tracker(request, land_project_pk):
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    land_project_trackers = Land_Projet_Tracker.objects.filter(land_project_id=land_project_pk)
    land_project_tracker_offers = Land_Projet_Tracker_Offer.objects.all().order_by('-created')
    if request.method == 'GET':
        return render(request, 'user/real_estate_projects/land_tracker/land_project_tracker.html',
                      {'land_project': land_project, 'land_project_tracker_offers': land_project_tracker_offers,
                       'land_project_trackers': land_project_trackers})


@login_required
def land_tracker_offer_detail(request, land_project_pk, land_project_tracker_pk, offer_pk):
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    land_project_tracker = get_object_or_404(Land_Projet_Tracker, pk=land_project_tracker_pk)
    land_project_tracker_offer = get_object_or_404(Land_Projet_Tracker_Offer, pk=offer_pk)
    offer_images = Land_Projet_Tracker_Offer_Image.objects.filter(project_tracker_offer_id=land_project_tracker_offer.id)
    land_plan_situation = Land_Plan_Situation.objects.all()
    land_papier_types = Land_Paper_Type.objects.all()
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        form = Land_Projet_Tracker_Offer_Form(instance=land_project_tracker_offer)
        return render(request, 'user/real_estate_projects/land_tracker/land_tracker_offer_detail.html',
                      {'land_project_tracker': land_project_tracker, 'land_project_tracker_offer':
                          land_project_tracker_offer, 'form': form, 'land_project': land_project,
                       'land_plan_situation': land_plan_situation, 'land_papier_types': land_papier_types,
                       'service_types': service_types, 'offer_images': offer_images})
    else:
        try:
            form = Land_Projet_Tracker_Offer_Form(request.POST, instance=land_project_tracker_offer)

            if 'offer_accepted' in request.POST:
                form = form.save(commit=False)
                form.land_project_tacker = get_object_or_404(Land_Projet_Tracker,
                                                id=request.POST.get('land_project_tracker_id'))
                form.save()
                messages.success(request, 'Cette offre a été acceptée avec succès !')
                return redirect('land_project_tracker', land_project_pk=land_project_pk)

        except ValueError:
            return render(request, 'user/real_estate_projects/land_tracker/land_tracker_offers.html',
                          {'land_project_tracker': land_project_tracker, 'land_project_tracker_offer':
                          land_project_tracker_offer, 'form': form, 'land_project': land_project,
                           'land_plan_situation': land_plan_situation, 'land_papier_types': land_papier_types,
                           'service_types': service_types, 'offer_images': offer_images,
                           'error': 'Une erreur est survenue !'})


@login_required
def land_tracker_offer_payment(request, land_project_pk, land_project_tracker_pk, offer_pk):
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    land_project_tracker = get_object_or_404(Land_Projet_Tracker, pk=land_project_tracker_pk)
    land_project_tracker_offer = get_object_or_404(Land_Projet_Tracker_Offer, pk=offer_pk)
    land_tracker_offer_payment = Land_Projet_Tracker_Offer_Payment.objects.filter(
                                    project_tracker_offer_id=offer_pk)
    land_tracker_offer_payment_images = Land_Projet_Tracker_Payment_Image.objects.all()
    if request.method == 'GET':
        return render(request, 'user/real_estate_projects/land_tracker/land_tracker_offer_payment.html',
                      {'land_tracker_offer_payment': land_tracker_offer_payment, 'land_project_tracker_offer':
                       land_project_tracker_offer, 'land_project': land_project, 'land_project_tracker':
                       land_project_tracker, 'land_tracker_offer_payment_images':
                       land_tracker_offer_payment_images})

###########################################END LAND PROJECT TRACKER#############################################
###########################################END LAND PROJECT TRACKER#############################################
###########################################END LAND PROJECT TRACKER#############################################





@login_required
def cart(request):
    lands = Lands.objects.all()
    properties = Property.objects.all()
    land_projects = Land_Project.objects.all()
    service_types = Service_Type.objects.all()
    images = Land_Images1.objects.all()
    land_types = Land_Type.objects.filter()
    cart = Cart.objects.all()
    property_types = Property_Type.objects.all()
    land_plan_situation = Land_Plan_Situation.objects.all()
    land_papier_types = Land_Paper_Type.objects.all()
    property_type_details_images = Property_Type_Details_Image.objects.all()
    property_type_details = Property_Type_Details.objects.all()

    return render(request, 'user/cart/cart.html', {'lands': lands, 'land_projects':
            land_projects, 'land_types': land_types, 'images': images, 'cart': cart, 'properties': properties,
             'land_plan_situation': land_plan_situation, 'land_papier_types': land_papier_types, 'property_types':
                                                       property_types, 'property_type_details_images': property_type_details_images,
                                                   'property_type_details': property_type_details,
                                                                   'service_types':
                                                                       service_types})


@login_required
def cart_payment(request, land_pk):
    land = Lands.objects.filter(id=land_pk)
    properties = Property.objects.all()
    land_projects = Land_Project.objects.all()
    service_types = Service_Type.objects.all()
    images = Land_Images1.objects.all()
    land_types = Land_Type.objects.filter()
    cart = Cart.objects.all().order_by('-created')

    land_plan_situation = Land_Plan_Situation.objects.all()
    land_papier_types = Land_Paper_Type.objects.all()

    return render(request, 'user/cart/cart_payment.html', {'land': land, 'land_projects':
            land_projects, 'land_types': land_types, 'images': images, 'cart': cart, 'properties': properties,
             'land_plan_situation': land_plan_situation, 'land_papier_types': land_papier_types,
                                                                   'service_types':
                                                                       service_types})


#############################################Construction projects###############################################
#############################################Construction projects###############################################
#############################################Construction projects###############################################
@login_required
def construction_projects(request):
    construction_projects = Construction_Project.objects.filter(user=request.user).order_by('-created')
    construction_type = Construction_Type.objects.all()
    return render(request, 'user/construction_projects/construction_projects.html', {
        'construction_projects': construction_projects, 'construction_type': construction_type})


@login_required
def construction_project_detail(request, construction_project_pk):
    construction_project_services = Construction_Service.objects.all()
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    construction_types = Construction_Type.objects.all()
    construction_floors = Construction_floor.objects.all()
    images = Architecture_Image.objects.all()
    tracker = get_object_or_404(Construction_Projet_Tracker, construction_project_id=construction_project_pk)

    return render(request, 'user/construction_projects/construction_project_detail.html',
                  {'construction_project': construction_project, 'construction_types': construction_types,
                   'construction_floors': construction_floors, 'images': images, 'tracker': tracker,
                   'construction_project_services': construction_project_services})


@login_required
def edit_construction_floor(request, construction_project_pk, construction_floor_pk):
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    #land_construction = Lands.objects.all()
    construction_types = Construction_Type.objects.all()
    land_papier_types = Land_Paper_Type.objects.all()
    land_plan_situation = Land_Plan_Situation.objects.all()
    construction_floor = get_object_or_404(Construction_floor, id=construction_floor_pk)

    if request.method == 'GET':
        form_construction_floor_project = Construction_floor_Form(instance=construction_floor)
        return render(request, 'user/construction_projects/edit_construction_floor.html',
                      {'construction_project': construction_project, 'form_construction_floor_project':
                          form_construction_floor_project, 'construction_floor': construction_floor,
                           'construction_types': construction_types,
                           'land_papier_types': land_papier_types,
                           'land_plan_situation': land_plan_situation})
    else:
        try:
            form_construction_floor_project = Construction_floor_Form(request.POST, instance=construction_floor)
            if form_construction_floor_project.is_valid():
                #Saving the land infos for the consruction project#
                form_construction_floor_project = form_construction_floor_project.save(commit=False)
                form_construction_floor_project.construction_project = get_object_or_404(Construction_Project,
                                                             id=construction_project_pk)
                form_construction_floor_project.save()
                messages.success(request, 'Modificatin effectuée avec succès !')
                return redirect('construction_project_detail', construction_project_pk=construction_project_pk)

        except ValueError:
            return render(request, 'user/construction_projects/edit_construction_floor.html',
                          {'construction_project': construction_project, 'construction_floor': construction_floor,
                           'construction_types': construction_types,
                           'land_papier_types': land_papier_types,
                           'land_plan_situation': land_plan_situation, 'error': 'Mauvaises données saisies !'})


@login_required
def delete_construction_floor(request, construction_project_pk, construction_floor_pk):
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    construction_floor = get_object_or_404(Construction_floor, id=construction_floor_pk)

    if request.method == 'GET':
        return render(request, 'user/construction_projects/delete_construction_floor.html',
                      {'construction_project':
                                        construction_project, 'construction_floor': construction_floor})
    if request.method == 'POST':
        construction_floor.delete()
        messages.success(request, 'Suppression effectuée !')
        return redirect('construction_project_detail', construction_project_pk=construction_project_pk)


@login_required
def construction_project_deletion(request, construction_project_pk):
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    construction_types = Construction_Type.objects.all()

    if request.method == 'GET':
        return render(request, 'user/construction_projects/construction_project_deletion.html',
                      {'construction_project':
                                        construction_project, 'construction_types': construction_types})
    if request.method == 'POST':
        construction_project.delete()
        messages.success(request, 'Suppression effectuée !')
        return redirect('construction_projects')
#########################################End Construction projects###############################################
#########################################End Construction projects###############################################
#########################################End Construction projects###############################################


##########################################Architecture project Tracker###########################################
##########################################Architecture project Tracker###########################################
##########################################Architecture project Tracker###########################################
@login_required
def projet_architecture_tracker(request, construction_project_pk, tracker_pk):
    construction_project_services = Construction_Service.objects.all()
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    architecture_project_tracker = Architecture_Project_Tracker.objects.filter(construction_project_id=construction_project_pk)
    images = Architecture_Project_Tracker_Image.objects.all()

    if request.method == 'GET':
        return render(request, 'user/construction_projects/tracker/architecture/projet_architecture_tracker.html',
                      {'construction_project': construction_project, 'construction_project_services': construction_project_services,
                       'architecture_project_tracker': architecture_project_tracker, 'images': images
                       })

####################################End Architecture project Tracker#############################################
####################################End Architecture project Tracker#############################################
####################################End Architecture project Tracker#############################################



##########################################Construction project Tracker###########################################
##########################################Construction project Tracker###########################################
##########################################Construction project Tracker###########################################
@login_required
def construction_project_tracker(request, construction_project_pk, tracker_pk):
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    tracker = get_object_or_404(Construction_Projet_Tracker, pk=tracker_pk)
    construction_types = Construction_Type.objects.all()
    construction_tracker_steps = Construction_Tracker_Step.objects.all()
    construction_tracker_sub_steps = Construction_Tracker_Sub_Step.objects.all().order_by('-id')

    construction_tracker_realisations = Construction_Tracker_Realisation.objects.filter(construction_project_tracker_id=tracker.id)
    construction_tracker_realisations_count = Construction_Tracker_Realisation.objects.filter\
        (construction_project_tracker_id=tracker.id).count()
    construction_tracker_realisation_last = Construction_Tracker_Realisation.objects.filter(construction_project_tracker_id=tracker.id).last()
    construction_tracker_realisation_images = Construction_Tracker_Realisation_Image.objects.all()
    construction_expense_payments = Construction_Expense.objects.filter(construction_project_tracker_id=tracker.id) \
        .order_by('-created')
    step_realisation_payments = Step_Payment.objects.filter(construction_project_tracker_id=tracker.id) \
        .order_by('-created')
    construction_delivery_payment = Delivery_Payment.objects.all().order_by('-created')
    if request.method == 'GET':
        return render(request, 'user/construction_projects/tracker/construction_project_tracker.html',
                      {'construction_project': construction_project, 'construction_types': construction_types,
                       'tracker': tracker, 'construction_tracker_steps': construction_tracker_steps,
                        'construction_tracker_sub_steps':
                           construction_tracker_sub_steps, 'construction_tracker_realisations':
                           construction_tracker_realisations, 'construction_tracker_realisation_images':
                           construction_tracker_realisation_images, 'construction_tracker_realisation_last':
                           construction_tracker_realisation_last, 'construction_tracker_realisations_count':
                           construction_tracker_realisations_count, 'construction_expense_payments':
                           construction_expense_payments, 'step_realisation_payments': step_realisation_payments,
                       'construction_delivery_payment': construction_delivery_payment
                       })


@login_required
def construction_project_realisation_gallery(request, construction_project_pk, tracker_pk):
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    tracker = get_object_or_404(Construction_Projet_Tracker, pk=tracker_pk)
    construction_types = Construction_Type.objects.all()
    construction_tracker_steps = Construction_Tracker_Step.objects.all()
    construction_tracker_sub_steps = Construction_Tracker_Sub_Step.objects.all()

    construction_tracker_realisations = Construction_Tracker_Realisation.objects.filter(construction_project_tracker_id=tracker.id)
    construction_tracker_realisation_images = Construction_Tracker_Realisation_Image.objects.all()
    if request.method == 'GET':
        return render(request, 'user/construction_projects/tracker/construction_project_realisation_gallery.html',
                      {'construction_project': construction_project, 'construction_types': construction_types,
                       'tracker': tracker, 'construction_tracker_steps': construction_tracker_steps,
                        'construction_tracker_sub_steps':
                           construction_tracker_sub_steps, 'construction_tracker_realisations':
                           construction_tracker_realisations, 'construction_tracker_realisation_images':
                           construction_tracker_realisation_images
                       })
####################################End Construction project Tracker#############################################
####################################End Construction project Tracker#############################################
####################################End Construction project Tracker#############################################





#################################Construction project Automatic counter##########################################
#################################Construction project Automatic counter##########################################
#################################Construction project Automatic counter##########################################
@login_required
def construction_project_automatic_counter(request, construction_project_pk, tracker_pk):
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    tracker = get_object_or_404(Construction_Projet_Tracker, pk=tracker_pk)
    construction_types = Construction_Type.objects.all()
    construction_tracker_steps = Construction_Tracker_Step.objects.all()
    construction_tracker_sub_steps = Construction_Tracker_Sub_Step.objects.all().order_by('-id')
    construction_tracker_realisations = Construction_Tracker_Realisation.objects.filter(construction_project_tracker_id
                                                                                        =tracker.id)
    construction_expense_payments = Construction_Expense.objects.filter(construction_project_tracker_id=tracker.id)\
                                    .order_by('-created')
    step_realisation_payments = Step_Payment.objects.filter(construction_project_tracker_id=tracker.id) \
        .order_by('-created')
    #contruction delivery#
    construction_delivery = Construction_Delivery.objects.filter(construction_project_tracker_id=tracker.id)
    construction_delivery_payment = Delivery_Payment.objects.all().order_by('-created')
    #automatic counter
    if construction_expense_payments:
        construction_expense_payment_sum = Construction_Expense.objects.filter(construction_project_tracker_id=tracker.id) \
            .aggregate(Sum('amount'))['amount__sum']

        if step_realisation_payments:
            construction_step_payment_sum = Step_Payment.objects.filter(construction_project_tracker_id=tracker.id) \
                .aggregate(Sum('amount'))['amount__sum']
            if construction_delivery:
                for delivery in construction_delivery:
                    for delivery_payment in construction_delivery_payment:
                        if delivery_payment.construction_delivery_id == delivery.id:
                            total_payment_deliveries = \
                            Delivery_Payment.objects.filter(construction_delivery_id=delivery.id).aggregate(
                                Sum('amount'))['amount__sum']
                            total = construction_expense_payment_sum + construction_step_payment_sum
                            total = total + total_payment_deliveries

                            return render(request,
                                          'user/construction_projects/automatic_counter/construction_project_automatic_counter'
                                          '.html',
                                          {'construction_project': construction_project,
                                           'construction_types': construction_types,
                                           'tracker': tracker, 'construction_tracker_steps': construction_tracker_steps,
                                           'construction_tracker_sub_steps': construction_tracker_sub_steps,
                                           'construction_tracker_realisations': construction_tracker_realisations,
                                           'construction_expense_payments':
                                               construction_expense_payments,
                                           'step_realisation_payments': step_realisation_payments,
                                           'construction_delivery':
                                               construction_delivery,
                                           'construction_delivery_payment': construction_delivery_payment, 'total': total
                                           })

            else:
                total = construction_expense_payment_sum + construction_step_payment_sum
        else:
            total = construction_expense_payment_sum
    else:
        total = 0

    if request.method == 'GET':
        return render(request, 'user/construction_projects/automatic_counter/construction_project_automatic_counter'
                               '.html',
                      {'construction_project': construction_project, 'construction_types': construction_types,
                       'tracker': tracker, 'construction_tracker_steps': construction_tracker_steps,
                        'construction_tracker_sub_steps': construction_tracker_sub_steps,
                       'construction_tracker_realisations': construction_tracker_realisations, 'construction_expense_payments':
                           construction_expense_payments, 'step_realisation_payments': step_realisation_payments,
                        'construction_delivery':
                           construction_delivery, 'construction_delivery_payment': construction_delivery_payment,
                       'total': total
                       })


@login_required
def construction_project_deliveries(request, construction_project_pk, tracker_pk):
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    tracker = get_object_or_404(Construction_Projet_Tracker, pk=tracker_pk)
    providers = Provider.objects.all()
    construction_delivery = Construction_Delivery.objects.filter(construction_project_tracker_id=tracker.id)
    construction_delivery_payment = Delivery_Payment.objects.all().order_by('-created')
    construction_delivery_images = Construction_Delivery_Image.objects.all()
    if request.method == 'GET':
        return render(request, 'user/construction_projects/automatic_counter/construction_project_deliveries'
                               '.html',
                      {'construction_project': construction_project, 'providers': providers,
                       'tracker': tracker, 'construction_delivery_images': construction_delivery_images,
                        'construction_delivery': construction_delivery, 'construction_delivery_payment':
                           construction_delivery_payment,
                       })


@login_required
def construction_delivery_details(request, construction_project_pk, tracker_pk, delivery_pk):
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    tracker = get_object_or_404(Construction_Projet_Tracker, pk=tracker_pk)
    construction_delivery = get_object_or_404(Construction_Delivery, pk=delivery_pk)
    providers = Provider.objects.all()
    construction_delivery_payment = Delivery_Payment.objects.filter(construction_delivery_id=construction_delivery.id)
    construction_delivery_images = Construction_Delivery_Image.objects.filter(construction_delivery_id=delivery_pk)
    if request.method == 'GET':
        return render(request, 'user/construction_projects/automatic_counter/construction_delivery_details'
                               '.html',
                      {'construction_project': construction_project, 'providers': providers,
                       'tracker': tracker, 'construction_delivery_images': construction_delivery_images,
                        'construction_delivery': construction_delivery, 'construction_delivery_payment':
                           construction_delivery_payment,
                       })
################################End Construction project Automatic counter#######################################
################################End Construction project Automatic counter#######################################
################################End Construction project Automatic counter#######################################