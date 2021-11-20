import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from real_estate.forms import Land_Form, Property_Form, Property_Type_Detail_Form, Property_Type_Detail_Image_Form, Land_Images1_Form, Cart_Form
from real_estate.models import Land_Type, Land_Project, Service_Type, Land_Plan_Situation, Lands, \
    Real_Estate_Projet_Type, Land_Images1, Property_Type, Property, Land_Paper_Type, Property_Type_Details_Image, \
    Property_Type_Details
from user.models import Customer, Cart, Land_Projet_Tracker, Property_Projet_Tracker


def real_estate(request):
    return render(request, 'real_estate/real_estate.html')

    ###############################Land###################


def land_project(request):
    land_type = Land_Type.objects.all()
    service_type = Service_Type.objects.all()
    lands = Lands.objects.all()
    service_types = Service_Type.objects.all()
    land_project = Land_Project.objects.all()
    land_plan_situation = Land_Plan_Situation.objects.all()
    cart_count = Cart.objects.all()

    if request.method == 'GET':
        form = Cart_Form(request.POST)
        return render(request, 'real_estate/land/land_project.html',
                      {'land_type': land_type, 'service_type': service_type, 'form': form,
                       'lands': lands, 'service_types': service_types,
                       'land_project': land_project, 'land_plan_situation':
                           land_plan_situation, 'cart_count': cart_count})
    else:
        try:
            if request.user.is_authenticated:
                if 'add_cart' in request.POST:
                    form = Cart_Form(request.POST)
                    if Cart.objects.filter(land_id=request.POST.get('land_id')):
                        messages.error(request, 'Erreur ! Ce terrain existe déjà dans votre panier !')
                        return redirect('land_project')
                    else:
                        form = form.save(commit=False)
                        form.user = request.user
                        form.save()
                        messages.success(request, 'Ajout au panier éffectué !')
                        return redirect('land_project')

                land_type = get_object_or_404(Land_Type, id=request.POST.get('land_type_id'))
                service_type_object = get_object_or_404(Service_Type, id=request.POST.get('property_management_id'))
                real_estate_project_type = get_object_or_404(Real_Estate_Projet_Type,
                                                             name='Achat/Vente/Location de Terrains')

                customer_profile_verification = Customer.objects.filter(user=request.user)

                for customer in customer_profile_verification:
                    if customer.phone == "":
                        messages.error(request,
                                       'Votre Profile est imcomplet, veuillez renseigner votre numéro de téléphone avant de '
                                       'pouvoir faire un Achat/Vente/Location de Terrains !')
                        return redirect('profile')
                    else:
                        if customer.adress == "":
                            messages.error(request,
                                           'Votre Profile est imcomplet, veuillez renseigner votre adresse de résidence avant '
                                           'de pouvoir faire un Achat/Vente/Location de Terrains !')
                            return redirect('profile')
                        else:
                            if customer.country == "":
                                messages.error(request,
                                               'Votre Profile est imcomplet, veuillez renseigner votre pays de '
                                               'résidence avant de pouvoir faire un Achat/Vente/Location de Terrains !')
                                return redirect('profile')
                            else:

                                service_type_devis = get_object_or_404(Service_Type, id=request.POST.get('property_management_id'))
                                if service_type_devis.name == "Devis":
                                    messages.error(request, 'Le service de Devis est indisponible pour les Terrains !')
                                    return redirect('land_project')
                                else:
                                    new_land = Land_Project(service_type=service_type_object,
                                                            real_estate_project_type=real_estate_project_type,
                                                            land_type=land_type,
                                                            user=request.user)
                                    new_land.save()
                                    messages.success(request, 'Phase 1 terminée !')
                                    return redirect('land_operation_part1', land_project_pk=new_land.id)
            else:
                messages.error(request, 'Veuillez vous connectez pour pouvoir faire cette action !')
                return redirect('login_user')
        except ValueError:
            return render(request, 'real_estate/land/land_project.html',
                          {'land_type': land_type, 'service_type': service_type,
                           'lands': lands, 'service_types': service_types,
                           'land_project': land_project, 'land_plan_situation':
                               land_plan_situation, 'cart_count': cart_count, 'error': 'Mauvaises données saisies !'})


@login_required
def land_operation_part1(request, land_project_pk):
    customer_info = Customer.objects.filter(user=request.user)
    land_types = Land_Type.objects.filter()
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    service_types = Service_Type.objects.all()
    land_plan_situation = Land_Plan_Situation.objects.all()
    lands = Lands.objects.filter(land_project_id=land_project_pk)
    land_papier_types = Land_Paper_Type.objects.all()

    if request.method == 'GET':
        form = Land_Form()
        return render(request, 'real_estate/land/land_operation_part1.html',
                      {'customer_info': customer_info, 'land_project': land_project, 'land_types': land_types,
                       'form': form, 'service_types': service_types, 'land_plan_situation': land_plan_situation,
                       'land_project_pk': land_project_pk, 'lands': lands, 'land_papier_types':
                           land_papier_types})
    else:
        try:
            form = Land_Form(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.land_plan_situation = get_object_or_404(Land_Plan_Situation,
                                                             id=request.POST.get('land_plan_situation_id'))
                form.land_project = get_object_or_404(Land_Project, id=land_project_pk)
                form.land_paper_type = get_object_or_404(Land_Paper_Type, id=request.POST.get('land_paper_type_id'))
                form.save()
                # Creation of the land project tracker
                new_tracker = Land_Projet_Tracker(land_id=form.id, land_project_id=land_project_pk)
                new_tracker.save()

                messages.success(request, 'Nouveau terrain ajouté avec succès !')
                return redirect('land_operation_part1', land_project_pk=land_project_pk)
        except ValueError:
            return render(request, 'real_estate/land/land_operation_part1.html',
                          {'customer_info': customer_info, 'land_project': land_project, 'land_types': land_types,
                           'form': form, 'service_types': service_types, 'land_project_pk': land_project_pk,
                           'land_plan_situation': land_plan_situation, 'lands': lands,
                           'land_papier_types': land_papier_types, 'error': 'Mauvaises données saisies !'})


@login_required
def land_projet_deletion(request, land_project_pk):
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    service_types = Service_Type.objects.all()
    land_types = Land_Type.objects.filter()

    if request.method == 'GET':
        return render(request, 'real_estate/land/land_projet_deletion.html',
                      {'land_project':
                           land_project, 'land_types': land_types,
                       'service_types':
                           service_types, 'land_project_pk': land_project_pk})
    if request.method == 'POST':
        land_project.delete()
        messages.success(request, 'Suppression effectuée !')
        return redirect('land_project')


@login_required
def clone_land(request, land_project_pk, land_pk):
    customer_info = Customer.objects.filter(user=request.user)
    land = get_object_or_404(Lands, pk=land_pk)
    lands = Lands.objects.filter(land_project_id=land_project_pk)
    land_types = Land_Type.objects.filter()
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    service_types = Service_Type.objects.all()
    service_types_vente = Service_Type.objects.filter(name="Vente")  # sale
    service_types_location1 = Service_Type.objects.filter(name="Mise en Location d'un bien Immobilier/Terrain")
    service_types_location2 = Service_Type.objects.filter(name="Recherche de Location d'un logement/Terrain")
    service_types_achat = Service_Type.objects.filter(name="Achat")
    land_plan_situation = Land_Plan_Situation.objects.all()
    land_papier_types = Land_Paper_Type.objects.all()

    if request.method == 'GET':
        form = Land_Form()
        return render(request, 'real_estate/land/clone_land.html', {'land': land, 'form': form, 'land_project':
            land_project, 'land_types': land_types,
                                                                    'customer_info': customer_info, 'lands': lands,
                                                                    'service_types':
                                                                        service_types, 'land_plan_situation':
                                                                        land_plan_situation, 'service_types_vente':
                                                                        service_types_vente, 'service_types_location1':
                                                                        service_types_location1, 'service_types_achat':
                                                                        service_types_achat,
                                                                    'land_papier_types': land_papier_types,
                                                                    'service_types_location2': service_types_location2,
                                                                    'land_project_pk': land_project_pk})
    else:
        try:
            form = Land_Form(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.land_plan_situation = get_object_or_404(Land_Plan_Situation,
                                                             id=request.POST.get('land_plan_situation_id'))
                form.land_paper_type = get_object_or_404(Land_Paper_Type, id=request.POST.get('land_paper_type_id'))
                form.land_project = get_object_or_404(Land_Project, id=land_project_pk)
                form.save()
                messages.success(request, 'Clonage éffectuée !')
                return redirect('land_operation_part1', land_project_pk=land_project_pk)
        except ValueError:
            return render(request, 'real_estate/land/clone_land.html', {'land': land, 'form': form,
                                                                        'land_project':
                                                                            land_project, 'land_types': land_types,
                                                                        'service_types':
                                                                            service_types, 'land_plan_situation':
                                                                            land_plan_situation, 'customer_info':
                                                                            customer_info, 'lands': lands,
                                                                        'service_types_vente':
                                                                            service_types_vente,
                                                                        'service_types_location1':
                                                                            service_types_location1,
                                                                        'land_papier_types':
                                                                            land_papier_types,
                                                                        'service_types_achat':
                                                                            service_types_achat,
                                                                        'service_types_location2':
                                                                            service_types_location2,
                                                                        'land_project_pk': land_project_pk,
                                                                        'error': 'Mauvaises données saisies !'})


@login_required
def edit_land(request, land_project_pk, land_pk):
    customer_info = Customer.objects.filter(user=request.user)
    land = get_object_or_404(Lands, pk=land_pk)
    lands = Lands.objects.filter(land_project_id=land_project_pk)
    land_types = Land_Type.objects.filter()
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    service_types = Service_Type.objects.all()
    service_types_vente = Service_Type.objects.filter(name="Vente")  # sale
    service_types_location1 = Service_Type.objects.filter(name="Mise en Location d'un bien Immobilier/Terrain")
    service_types_location2 = Service_Type.objects.filter(name="Recherche de Location d'un logement/Terrain")
    service_types_achat = Service_Type.objects.filter(name="Achat")
    land_plan_situation = Land_Plan_Situation.objects.all()
    land_papier_types = Land_Paper_Type.objects.all()

    if request.method == 'GET':
        form = Land_Form(instance=land)
        return render(request, 'real_estate/land/edit_land.html', {'land': land, 'form': form, 'land_project':
            land_project, 'land_types': land_types,
                                                                   'customer_info': customer_info, 'lands': lands,
                                                                   'service_types':
                                                                       service_types, 'land_plan_situation':
                                                                       land_plan_situation, 'service_types_vente':
                                                                       service_types_vente, 'service_types_location1':
                                                                       service_types_location1, 'service_types_achat':
                                                                       service_types_achat, 'land_papier_types':
                                                                       land_papier_types,
                                                                   'service_types_location2': service_types_location2,
                                                                   'land_project_pk': land_project_pk})
    else:
        try:
            form = Land_Form(request.POST, instance=land)
            form = form.save(commit=False)
            form.land_plan_situation = get_object_or_404(Land_Plan_Situation,
                                                         id=request.POST.get('land_plan_situation_id'))
            form.land_paper_type = get_object_or_404(Land_Paper_Type, id=request.POST.get('land_paper_type_id'))
            form.land_project = get_object_or_404(Land_Project, id=land_project_pk)
            form.save()
            messages.success(request, 'Modification éffectuée !')
            return redirect('land_operation_part1', land_project_pk=land_project_pk)
        except ValueError:
            return render(request, 'real_estate/land/edit_land.html', {'land': land, 'form': form,
                                                                       'land_project':
                                                                           land_project, 'land_types': land_types,
                                                                       'service_types':
                                                                           service_types, 'land_plan_situation':
                                                                           land_plan_situation, 'customer_info':
                                                                           customer_info, 'lands': lands,
                                                                       'service_types_vente':
                                                                           service_types_vente, 'land_papier_types':
                                                                           land_papier_types,
                                                                       'service_types_location1':
                                                                           service_types_location1,
                                                                       'service_types_achat':
                                                                           service_types_achat,
                                                                       'service_types_location2': service_types_location2,
                                                                       'land_project_pk': land_project_pk,
                                                                       'error': 'Mauvaises données saisies !'})


@login_required
def delete_land(request, land_project_pk, land_pk):
    land = get_object_or_404(Lands, pk=land_pk)
    lands = Lands.objects.filter(land_project_id=land_project_pk)
    land_types = Land_Type.objects.filter()
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    service_types = Service_Type.objects.all()
    service_type_vente = Service_Type.objects.filter(name="Vente")  # sale
    land_plan_situation = Land_Plan_Situation.objects.all()
    service_types_location2 = Service_Type.objects.filter(name="Recherche de Location d'un logement/Terrain")
    land_papier_types = Land_Paper_Type.objects.all()

    if request.method == 'GET':
        return render(request, 'real_estate/land/delete_land.html',
                      {'land': land, 'land_project':
                          land_project, 'land_types': land_types, 'service_types_location2': service_types_location2,
                       'lands': lands, 'land_papier_types': land_papier_types,
                       'service_types':
                           service_types, 'land_plan_situation':
                           land_plan_situation, 'service_type_vente':
                           service_type_vente, 'land_project_pk': land_project_pk})
    if request.method == 'POST':
        land.delete()
        messages.success(request, 'Suppression effectuée !')
        return redirect('land_operation_part1', land_project_pk=land_project_pk)


def land_operation_part2(request, land_project_pk):
    customer_info = Customer.objects.filter(user=request.user)
    land_types = Land_Type.objects.filter()
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)
    service_types = Service_Type.objects.all()
    land_plan_situation = Land_Plan_Situation.objects.all()
    lands = Lands.objects.filter(land_project_id=land_project_pk)
    images = Land_Images1.objects.all()
    service_types_location2 = Service_Type.objects.filter(name="Recherche de Location d'un logement/Terrain")

    if 'complete_land_operation' in request.POST:
        if request.method == 'POST':
            messages.success(request, 'Votre demande a été envoyer avec succès, nous vous contacterons très bientôt  !')
            return redirect('project_detail', land_project_pk=land_project_pk)

    if request.method == 'GET':
        form = Land_Form()
        return render(request, 'real_estate/land/land_operation_part2.html',
                      {'customer_info': customer_info, 'land_project': land_project,
                       'land_types': land_types, 'service_types_location2': service_types_location2,
                       'form': form, 'service_types': service_types,
                       'land_plan_situation': land_plan_situation,
                        'land_project_pk': land_project_pk,
                       'lands': lands, 'images': images})
    else:
        try:
            form = Land_Images1_Form(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)
                form.land = get_object_or_404(Lands, id=request.POST.get('land_id'))
                form.save()
                messages.success(request, 'Image enregistrée avec succes !')
                return redirect('land_operation_part2', land_project_pk=land_project_pk)
        except ValueError:
            return render(request, 'real_estate/land/land_operation_part2.html',
                          {'customer_info': customer_info, 'land_project': land_project,
                           'land_types': land_types, 'service_types_location2': service_types_location2,
                           'form': form, 'service_types': service_types,
                           'land_project_pk': land_project_pk,
                           'land_plan_situation': land_plan_situation, 'lands': lands,
                           'images': images,
                           'error': 'Mauvaises données saisies !'})

        ###############################Land###################


def property_management(request):
    property_types = Property_Type.objects.all()
    service_types = Service_Type.objects.all()
    properties = Property.objects.all()
    property_type_details = Property_Type_Details.objects.all()
    property_type_details_images = Property_Type_Details_Image.objects.all()
    cart_count = Cart.objects.all()

    if request.method == 'GET':
        form = Property_Form()
        cart_form = Cart_Form(request.POST)

        # creation of the ref
        characters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        characters.extend(list('1234567890'))
        size = 10
        ref = ''
        for x in range(size):
            ref += random.choice(characters)
        ref = ref

        return render(request, 'real_estate/property_management/property_management.html',
                      {'property_types': property_types, 'form': form, 'service_types': service_types, 'properties':
                          properties, 'property_type_details': property_type_details, 'property_type_details_images': property_type_details_images,
                        'cart_count': cart_count, 'cart_form': cart_form, 'ref': ref})
    else:
        if request.user.is_authenticated:
            try:
                if 'add_cart' in request.POST:
                    cart_form = Cart_Form(request.POST)
                    if Cart.objects.filter(property_id=request.POST.get('property_id')):
                        messages.error(request, 'Erreur ! Ce terrain existe déjà dans votre panier !')
                        return redirect('property_management')
                    else:
                        cart_form = cart_form.save(commit=False)
                        cart_form.user = request.user
                        cart_form.save()
                        messages.success(request, 'Ajout au panier éffectué !')
                        return redirect('property_management')

                form = Property_Form(request.POST)
                property_type = get_object_or_404(Property_Type, id=request.POST.get('property_type_id'))
                service_type = get_object_or_404(Service_Type, id=request.POST.get('service_type_id'))

                if property_type.name == 'Chambre simple ou avec toilette':
                    if service_type.name == 'Vente' or service_type.name == 'Achat':
                        messages.error(request, 'Les services Vente et Achat sont indisponibles pour les chambres !')
                        return redirect('property_management')
                    if form.is_valid():
                        form = form.save(commit=False)
                        form.property_type = property_type
                        form.service_type = service_type
                        form.user = request.user
                        form.real_estate_project_type = get_object_or_404(Real_Estate_Projet_Type,
                                                                          name='Achat/Vente/Location de biens Immobilier')
                        form.save()
                        # Creation of the property project tracker
                        new_tracker = Property_Projet_Tracker(property_id=form.id)
                        new_tracker.save()

                        messages.success(request, 'Phase 1 terminée !')
                        return redirect('property_management_part1', property_pk=form.id)

                else:
                    if form.is_valid():
                        form = form.save(commit=False)
                        form.property_type = property_type
                        form.service_type = service_type
                        form.user = request.user
                        form.real_estate_project_type = get_object_or_404(Real_Estate_Projet_Type,
                                                                          name='Achat/Vente/Location de biens Immobilier')
                        form.save()

                        # Creation of the property project tracker
                        new_tracker = Property_Projet_Tracker(property_id=form.id)
                        new_tracker.save()

                        messages.success(request, 'Phase 1 terminée !')
                        return redirect('property_management_part1', property_pk=form.id)
            except ValueError:
                return render(request, 'real_estate/property_management/property_management.html',
                              {'property_types': property_types, 'form': form, 'service_types': service_types,
                               'properties':
                                   properties, 'property_type_details': property_type_details, 'property_type_details_images':
                                   property_type_details_images, 'cart_count': cart_count, 'cart_form': cart_form,
                               'error': 'Mauvaises données saisies !'})
        else:
            messages.error(request, 'Veuillez vous connectez pour pouvoir faire cette action !')
            return redirect('login_user')

            # Property management apartments#


@login_required
def property_management_part1(request, property_pk):
    property = get_object_or_404(Property, pk=property_pk, user=request.user)
    service_types = Service_Type.objects.all()
    property_types = Property_Type.objects.all()
    property_type_details = Property_Type_Details.objects.filter(property_id=property_pk)

    if 'complete_land_operation' in request.POST:
        if request.method == 'POST':
            messages.success(request, 'Votre demande a été envoyer avec accès , nous vous contacterons très bientôt !')
            return redirect('profile')

    if request.method == 'GET':
        property_type_form = Property_Type_Detail_Form()
        return render(request, 'real_estate/property_management/property_management_part1.html',
                      {'property': property, 'property_type_details': property_type_details, 'property_type_form': property_type_form,
                       'service_types': service_types, 'property_types': property_types})
    else:
        try:
            property_type_form = Property_Type_Detail_Form(request.POST)
            if request.user.is_authenticated:
                if property_type_form.is_valid():
                    property_type_form = property_type_form.save(commit=False)
                    property_type_form.property = property
                    property_type_form.save()
                    messages.success(request, 'Informations enregistrées !')
                    return redirect('property_management_part1', property_pk=property_pk)

            else:
                messages.error(request, 'Veuillez vous connectez pour pouvoir faire cette action !')
                return redirect('login_user')

        except ValueError:
            return render(request, 'real_estate/property_management/property_management_part1.html',
                          {'property': property, 'property_type_details': property_type_details, 'property_type_form': property_type_form,
                       'service_types': service_types, 'property_types': property_types,
                           'error': 'Mauvaises données saisies !'})


@login_required
def edit_property_type_details(request, property_pk, property_type_detail_pk):
    property = get_object_or_404(Property, pk=property_pk)
    property_type_details = get_object_or_404(Property_Type_Details, pk=property_type_detail_pk)
    service_types = Service_Type.objects.all()
    property_types = Property_Type.objects.all()

    if request.method == 'GET':
        form = Property_Type_Detail_Form(instance=property_type_details)
        return render(request, 'real_estate/property_management/edit_property_type_details.html', {'property_type_details': property_type_details,
                                                                                       'form': form, 'service_types':
                                                                                           service_types, 'property_types': property_types,
                                                                                       'property': property})
    else:
        try:
            form = Property_Type_Detail_Form(request.POST, instance=property_type_details)
            form = form.save(commit=False)
            form.property = get_object_or_404(Property, id=property_pk)
            form.save()
            messages.success(request, 'Modification éffectuée !')
            return redirect('property_management_part1', property_pk=property_pk)
        except ValueError:
            return render(request, 'real_estate/property_management/edit_property_type_details.html',
                          {'property_type_details': property_type_details, 'form': form, 'property_types': property_types,
                           'property': property, 'service_types': service_types,
                           'error': 'Mauvaises données saisies !'})



@login_required
def property_management_deletion(request, property_pk):
    property = get_object_or_404(Property, pk=property_pk)
    service_types = Service_Type.objects.all()
    property_types = Property_Type.objects.all()

    if request.method == 'GET':
        return render(request, 'real_estate/property_management/property_management_deletion.html',
                      {'property': property, 'service_types': service_types, 'property_types':
                          property_types})
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Suppression effectuée !')
        return redirect('property_management')


def property_management_part2(request, property_pk):
    property = get_object_or_404(Property, pk=property_pk, user=request.user)
    service_types = Service_Type.objects.all()
    property_type_details_images = Property_Type_Details_Image.objects.all()
    property_types = Property_Type.objects.all()
    property_type_details = Property_Type_Details.objects.filter(property_id=property_pk)

    if 'complete_land_operation' in request.POST:
        if request.method == 'POST':
            messages.success(request, 'Votre demande a été envoyer avec accès , nous vous contacterons très bientôt !')
            return redirect('profile')

    if request.method == 'GET':
        property_type_image_form = Property_Type_Detail_Image_Form()

        return render(request, 'real_estate/property_management/property_management_part2.html',
                      {'property': property, 'property_type_image_form': property_type_image_form,
                       'property_type_details': property_type_details, 'service_types': service_types,
                       'property_types': property_types, 'property_type_details_images': property_type_details_images})
    else:
        try:
            property_type_image_form = Property_Type_Detail_Image_Form(request.POST, request.FILES)

            if 'image_submit' in request.POST:
                if property_type_image_form.is_valid():
                    property_type_image_form = property_type_image_form.save(commit=False)
                    property_type_image_form.property_type_detail = get_object_or_404(Property_Type_Details, id=request.POST.get('property_type_detail_id'))
                    property_type_image_form.save()
                    messages.success(request, 'Image enregistrée avec succès !')
                    return redirect('property_management_part2', property_pk=property_pk)

        except ValueError:
            return render(request, 'real_estate/property_management/property_management_part2.html',
                          {'property': property, 'property_type_image_form': property_type_image_form,
                       'property_type_details': property_type_details, 'service_types': service_types,
                       'property_types': property_types, 'property_type_details_images': property_type_details_images,
                           'error': 'Mauvaises données saisies !'})


@login_required
def land_ad_detail(request, land_project_pk, land_pk):
    land = get_object_or_404(Lands, pk=land_pk)
    service_types = Service_Type.objects.all()
    images = Land_Images1.objects.all()
    land_types = Land_Type.objects.filter()
    land_project = get_object_or_404(Land_Project, pk=land_project_pk, user=request.user)

    land_plan_situation = Land_Plan_Situation.objects.all()
    land_papier_types = Land_Paper_Type.objects.all()
    cart_count = Cart.objects.filter(user=request.user)

    if request.method == 'GET':
        form = Cart_Form()
        return render(request, 'real_estate/land/land_ad_detail.html', {'land': land, 'land_project':
            land_project, 'land_types': land_types, 'images': images, 'form': form, 'cart_count': cart_count,
                                                                        'service_types':
                                                                            service_types, 'land_plan_situation':
                                                                            land_plan_situation, 'land_papier_types':
                                                                            land_papier_types,
                                                                        'land_project_pk': land_project_pk})
    else:
        try:
            form = Cart_Form(request.POST)
            if Cart.objects.filter(land_id=request.POST.get('land_id')):
                messages.error(request, 'Erreur ! Ce terrain existe déjà dans votre panier !')
                return redirect('land_project')
            else:
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                messages.success(request, 'Ajout au panier éffectué !')
                return redirect('land_project')
        except ValueError:
            return render(request, 'real_estate/land/land_ad_detail.html',
                          {'land': land, 'land_project':
                              land_project, 'cart_count': cart_count, 'land_types': land_types, 'images': images,
                           'form': form,
                           'service_types':
                               service_types, 'land_plan_situation':
                               land_plan_situation, 'land_papier_types':
                               land_papier_types,
                           'land_project_pk': land_project_pk,
                           'error': 'Mauvaises données saisies !'})


@login_required
def property_management_ad_detail(request, property_pk, property_type_detail_pk):
    property = get_object_or_404(Property, pk=property_pk)
    property_type_detail = get_object_or_404(Property_Type_Details, pk=property_type_detail_pk)
    property_type_details_images = Property_Type_Details_Image.objects.filter(property_type_detail_id=property_type_detail_pk)
    service_types = Service_Type.objects.all()
    cart_count = Cart.objects.filter(user=request.user)
    property_types = Property_Type.objects.all()

    if request.method == 'GET':
        form = Cart_Form()
        return render(request, 'real_estate/property_management/property_management_ad_detail.html',
                      {'property': property, 'property_type_detail': property_type_detail,
                       'property_type_details_images': property_type_details_images, 'form': form, 'cart_count': cart_count,
                       'service_types':
                           service_types, 'property_types': property_types})
    else:
        try:
            form = Cart_Form(request.POST)
            if Cart.objects.filter(property_id=request.POST.get('property_id')):
                messages.error(request, 'Erreur ! Ce bien immobilier existe déjà dans votre panier !')
                return redirect('property_management')
            else:
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                messages.success(request, 'Ajout au panier éffectué !')
                return redirect('property_management')
        except ValueError:
            return render(request, 'real_estate/property_management/property_management_ad_detail.html',
                          {'property': property, 'property_type_detail': property_type_detail,
                       'property_type_details_images': property_type_details_images, 'form': form, 'cart_count': cart_count,
                       'service_types': service_types, 'property_types': property_types,
                           'error': 'Mauvaises données saisies !'})