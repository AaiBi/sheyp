from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from real_estate.forms import Land_Form, Property_Form, Apartment_Form, Apartment_Image_Form, Land_Images1_Form, \
    Studio_Form, Studio_Image_Form, House_Form, House_Image_Form, Room_Form, Room_Image_Form, Cart_Form
from real_estate.models import Land_Type, Land_Project, Service_Type, Land_Plan_Situation, Lands, \
    Real_Estate_Projet_Type, Land_Images1, Property_Type, Property, Apartment, Studio, \
    Studio_Image, Land_Paper_Type, Apartment_Image, House, House_Image, Room, Room_Image
from user.models import Customer, Cart, Land_Projet_Tracker


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
    apartments = Apartment.objects.all()
    apartment_images = Apartment_Image.objects.all()
    studios = Studio.objects.all()
    studio_image = Studio_Image.objects.all()
    houses = House.objects.all()
    house_images = House_Image.objects.all()
    rooms = Room.objects.all()
    room_images = Room_Image.objects.all()
    cart_count = Cart.objects.all()

    if request.method == 'GET':
        form = Property_Form()
        cart_form = Cart_Form(request.POST)
        return render(request, 'real_estate/property_management/property_management.html',
                      {'property_types': property_types, 'form': form, 'service_types': service_types, 'properties':
                          properties, 'apartments': apartments, 'apartment_images': apartment_images,
                       'studios': studios,
                       'studio_image': studio_image, 'houses': houses, 'house_images': house_images, 'rooms': rooms,
                       'room_images': room_images, 'cart_count': cart_count, 'cart_form': cart_form})
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
                else:
                    if form.is_valid():
                        form = form.save(commit=False)
                        form.property_type = property_type
                        form.service_type = service_type
                        form.user = request.user
                        form.real_estate_project_type = get_object_or_404(Real_Estate_Projet_Type,
                                                                          name='Achat/Vente/Location de biens Immobilier')
                        form.save()
                        messages.success(request, 'Phase 1 terminée !')
                        return redirect('property_management_part1', property_pk=form.id)
            except ValueError:
                return render(request, 'real_estate/property_management/property_management.html',
                              {'property_types': property_types, 'form': form, 'service_types': service_types,
                               'properties':
                                   properties, 'apartments': apartments, 'apartment_images': apartment_images,
                               'studios': studios,
                               'studio_image': studio_image, 'houses': houses, 'house_images': house_images,
                               'rooms': rooms,
                               'room_images': room_images, 'cart_count': cart_count, 'cart_form': cart_form,
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
    apartments = Apartment.objects.filter(property_id=property_pk)
    studios = Studio.objects.filter(property_id=property_pk)
    houses = House.objects.filter(property_id=property_pk)
    rooms = Room.objects.filter(property_id=property_pk)

    if request.method == 'GET':
        apartment_form = Apartment_Form()
        studio_form = Studio_Form()
        house_form = House_Form()
        room_form = Room_Form()
        return render(request, 'real_estate/property_management/property_management_part1.html',
                      {'property': property, 'studio_form': studio_form, 'studios': studios, 'houses': houses,
                       'apartment_form': apartment_form, 'service_types': service_types, 'house_form': house_form,
                       'property_types': property_types, 'apartments': apartments, 'room_form': room_form, 'rooms':
                           rooms})
    else:
        try:
            apartment_form = Apartment_Form(request.POST)
            studio_form = Studio_Form(request.POST)
            house_form = House_Form(request.POST)
            room_form = Room_Form(request.POST)
            if request.user.is_authenticated:
                if apartment_form.is_valid():
                    apartment_form = apartment_form.save(commit=False)
                    apartment_form.property = property
                    apartment_form.save()
                    messages.success(request, 'Nouvel appartement enregistré !')
                    return redirect('property_management_part1', property_pk=property_pk)

                if studio_form.is_valid():
                    studio_form = studio_form.save(commit=False)
                    studio_form.property = property
                    studio_form.save()
                    messages.success(request, 'Nouveau studio enregistré !')
                    return redirect('property_management_part1', property_pk=property_pk)

                if house_form.is_valid():
                    house_form = house_form.save(commit=False)
                    house_form.property = property
                    house_form.save()
                    messages.success(request, 'Nouvelle maison enregistrée !')
                    return redirect('property_management_part1', property_pk=property_pk)

                if room_form.is_valid():
                    room_form = room_form.save(commit=False)
                    room_form.property = property
                    room_form.save()
                    messages.success(request, 'Nouvelle chambre enregistrée !')
                    return redirect('property_management_part1', property_pk=property_pk)
            else:
                messages.error(request, 'Veuillez vous connectez pour pouvoir faire cette action !')
                return redirect('login_user')

        except ValueError:
            return render(request, 'real_estate/property_management/property_management_part1.html',
                          {'property': property, 'studio_form': studio_form, 'studios': studios, 'houses': houses,
                           'apartment_form': apartment_form, 'service_types': service_types, 'apartments': apartments,
                           'property_types': property_types, 'house_form': house_form, 'room_form': room_form, 'rooms':
                               rooms,
                           'error': 'Mauvaises données saisies !'})


@login_required
def edit_apartment(request, property_pk, apartment_pk):
    property = get_object_or_404(Property, pk=property_pk)
    apartment = get_object_or_404(Apartment, pk=apartment_pk)
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        form = Apartment_Form(instance=apartment)
        return render(request, 'real_estate/property_management/edit_apartment.html', {'apartment': apartment,
                                                                                       'form': form, 'service_types':
                                                                                           service_types,
                                                                                       'property': property})
    else:
        try:
            form = Apartment_Form(request.POST, instance=apartment)
            form = form.save(commit=False)
            form.property = get_object_or_404(Property, id=property_pk)
            form.save()
            messages.success(request, 'Modification éffectuée !')
            return redirect('property_management_part1', property_pk=property_pk)
        except ValueError:
            return render(request, 'real_estate/property_management/edit_apartment.html',
                          {'apartment': apartment, 'form': form,
                           'property': property, 'service_types': service_types,
                           'error': 'Mauvaises données saisies !'})


@login_required
def clone_apartment(request, property_pk, apartment_pk):
    property = get_object_or_404(Property, pk=property_pk)
    apartment = get_object_or_404(Apartment, pk=apartment_pk)
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        form = Apartment_Form(instance=apartment)
        return render(request, 'real_estate/property_management/clone_apartment.html', {'apartment': apartment,
                                                                                        'form': form, 'service_types':
                                                                                            service_types,
                                                                                        'property': property})
    else:
        try:
            form = Apartment_Form(request.POST)
            form = form.save(commit=False)
            form.property = get_object_or_404(Property, id=property_pk)
            form.save()
            messages.success(request, 'Clonage éffectuée !')
            return redirect('property_management_part1', property_pk=property_pk)
        except ValueError:
            return render(request, 'real_estate/property_management/clone_apartment.html',
                          {'apartment': apartment, 'form': form,
                           'property': property, 'service_types': service_types,
                           'error': 'Mauvaises données saisies !'})


@login_required
def delete_apartment(request, property_pk, apartment_pk):
    property = get_object_or_404(Property, pk=property_pk)
    apartment = get_object_or_404(Apartment, pk=apartment_pk)
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        return render(request, 'real_estate/property_management/delete_apartment.html',
                      {'apartment': apartment, 'property':
                          property, 'service_types': service_types})
    if request.method == 'POST':
        apartment.delete()
        messages.success(request, 'Suppression effectuée !')
        return redirect('property_management_part1', property_pk=property_pk)

        # Property management studios#


@login_required
def edit_studio(request, property_pk, studio_pk):
    property = get_object_or_404(Property, pk=property_pk)
    studio = get_object_or_404(Studio, pk=studio_pk)
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        form = Studio_Form(instance=studio)
        return render(request, 'real_estate/property_management/edit_studio.html', {'studio': studio,
                                                                                    'form': form, 'service_types':
                                                                                        service_types,
                                                                                    'property': property})
    else:
        try:
            form = Studio_Form(request.POST, instance=studio)
            form = form.save(commit=False)
            form.property = get_object_or_404(Property, id=property_pk)
            form.save()
            messages.success(request, 'Modification éffectuée !')
            return redirect('property_management_part1', property_pk=property_pk)
        except ValueError:
            return render(request, 'real_estate/property_management/edit_studio.html',
                          {'studio': studio, 'form': form,
                           'property': property, 'service_types': service_types,
                           'error': 'Mauvaises données saisies !'})


@login_required
def clone_studio(request, property_pk, studio_pk):
    property = get_object_or_404(Property, pk=property_pk)
    studio = get_object_or_404(Studio, pk=studio_pk)
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        form = Studio_Form(instance=studio)
        return render(request, 'real_estate/property_management/clone_studio.html', {'studio': studio,
                                                                                     'form': form, 'service_types':
                                                                                         service_types,
                                                                                     'property': property})
    else:
        try:
            form = Studio_Form(request.POST)
            form = form.save(commit=False)
            form.property = get_object_or_404(Property, id=property_pk)
            form.save()
            messages.success(request, 'Clonage éffectuée !')
            return redirect('property_management_part1', property_pk=property_pk)
        except ValueError:
            return render(request, 'real_estate/property_management/clone_studio.html',
                          {'studio': studio, 'form': form,
                           'property': property, 'service_types': service_types,
                           'error': 'Mauvaises données saisies !'})


@login_required
def delete_studio(request, property_pk, studio_pk):
    property = get_object_or_404(Property, pk=property_pk)
    studio = get_object_or_404(Studio, pk=studio_pk)
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        return render(request, 'real_estate/property_management/delete_studio.html',
                      {'studio': studio, 'property':
                          property, 'service_types': service_types})
    if request.method == 'POST':
        studio.delete()
        messages.success(request, 'Suppression effectuée !')
        return redirect('property_management_part1', property_pk=property_pk)


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
    apartments = Apartment.objects.filter(property_id=property_pk)
    apartments_images = Apartment_Image.objects.all()
    service_types = Service_Type.objects.all()
    property_types = Property_Type.objects.all()
    studios = Studio.objects.filter(property_id=property_pk)
    studio_images = Studio_Image.objects.all()
    house_images = House_Image.objects.all()
    houses = House.objects.filter(property_id=property_pk)
    rooms = Room.objects.filter(property_id=property_pk)
    room_images = Room_Image.objects.all()

    if 'complete_land_operation' in request.POST:
        if request.method == 'POST':
            messages.success(request, 'Votre demande a été envoyer avec accès , nous vous contacterons très bientôt !')
            return redirect('profile')

    if request.method == 'GET':
        apartment_image_form = Apartment_Image_Form()
        studio_image_form = Studio_Image_Form()
        house_image_form = House_Image_Form()
        room_image_form = Room_Image_Form()
        return render(request, 'real_estate/property_management/property_management_part2.html',
                      {'property': property, 'apartments': apartments, 'apartments_images': apartments_images,
                       'studio_image_form': studio_image_form, 'service_types': service_types,
                       'property_types': property_types,
                       'studios': studios, 'studio_images': studio_images, 'apartment_image_form':
                           apartment_image_form, 'house_image_form': house_image_form, 'house_images': house_images,
                       'houses': houses, 'rooms': rooms, 'room_image_form': room_image_form,
                       'room_images': room_images})
    else:
        try:
            studio_image_form = Studio_Image_Form(request.POST, request.FILES)
            apartment_image_form = Apartment_Image_Form(request.POST, request.FILES)
            house_image_form = House_Image_Form(request.POST, request.FILES)
            room_image_form = Room_Image_Form(request.POST, request.FILES)

            if 'apartment_image_submit' in request.POST:
                if apartment_image_form.is_valid():
                    apartment_image_form = apartment_image_form.save(commit=False)
                    apartment_image_form.apartment = get_object_or_404(Apartment, id=request.POST.get('apartment_id'))
                    apartment_image_form.save()
                    messages.success(request, 'Image enregistrée avec succès !')
                    return redirect('property_management_part2', property_pk=property_pk)

            if 'studio_image_submit' in request.POST:
                if studio_image_form.is_valid():
                    studio_image_form = studio_image_form.save(commit=False)
                    studio_image_form.studio = get_object_or_404(Studio, id=request.POST.get('studio_id'))
                    studio_image_form.save()
                    messages.success(request, 'Image enregistrée avec succès !')
                    return redirect('property_management_part2', property_pk=property_pk)

            if 'house_image_submit' in request.POST:
                if house_image_form.is_valid():
                    house_image_form = house_image_form.save(commit=False)
                    house_image_form.house = get_object_or_404(House, id=request.POST.get('house_id'))
                    house_image_form.save()
                    messages.success(request, 'Image enregistrée avec succès !')
                    return redirect('property_management_part2', property_pk=property_pk)

            if 'room_image_submit' in request.POST:
                if room_image_form.is_valid():
                    room_image_form = room_image_form.save(commit=False)
                    room_image_form.room = get_object_or_404(Room, id=request.POST.get('room_id'))
                    room_image_form.save()
                    messages.success(request, 'Image enregistrée avec succès !')
                    return redirect('property_management_part2', property_pk=property_pk)

        except ValueError:
            return render(request, 'real_estate/property_management/property_management_part2.html',
                          {'property': property, 'apartments': apartments, 'apartments_images': apartments_images,
                           'studio_image_form': studio_image_form, 'service_types': service_types,
                           'property_types': property_types,
                           'studios': studios, 'studio_images': studio_images, 'apartment_image_form':
                               apartment_image_form, 'house_image_form': house_image_form, 'house_images': house_images,
                           'houses': houses, 'rooms': rooms, 'room_image_form': room_image_form,
                           'room_images': room_images,
                           'error': 'Mauvaises données saisies !'})


################################################House########################################
@login_required
def edit_house(request, property_pk, house_pk):
    property = get_object_or_404(Property, pk=property_pk)
    house = get_object_or_404(House, pk=house_pk)
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        form = House_Form(instance=house)
        return render(request, 'real_estate/property_management/house/edit_house.html', {'house': house,
                                                                                         'form': form, 'service_types':
                                                                                             service_types,
                                                                                         'property': property})
    else:
        try:
            form = House_Form(request.POST, instance=house)
            form = form.save(commit=False)
            form.property = get_object_or_404(Property, id=property_pk)
            form.save()
            messages.success(request, 'Modification éffectuée !')
            return redirect('property_management_part1', property_pk=property_pk)
        except ValueError:
            return render(request, 'real_estate/property_management/house/edit_house.html',
                          {'house': house, 'form': form,
                           'property': property, 'service_types': service_types,
                           'error': 'Mauvaises données saisies !'})


def clone_house(request, property_pk, house_pk):
    property = get_object_or_404(Property, pk=property_pk)
    house = get_object_or_404(House, pk=house_pk)
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        form = House_Form()
        return render(request, 'real_estate/property_management/house/clone_house.html', {'house': house,
                                                                                          'form': form, 'service_types':
                                                                                              service_types,
                                                                                          'property': property})
    else:
        try:
            form = House_Form(request.POST)
            form = form.save(commit=False)
            form.property = get_object_or_404(Property, id=property_pk)
            form.save()
            messages.success(request, 'Clonage éffectuée !')
            return redirect('property_management_part1', property_pk=property_pk)
        except ValueError:
            return render(request, 'real_estate/property_management/house/clone_house.html',
                          {'house': house, 'form': form,
                           'property': property, 'service_types': service_types,
                           'error': 'Mauvaises données saisies !'})


def delete_house(request, property_pk, house_pk):
    property = get_object_or_404(Property, pk=property_pk)
    house = get_object_or_404(House, pk=house_pk)
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        return render(request, 'real_estate/property_management/house/delete_house.html', {'house': house,
                                                                                           'service_types':
                                                                                               service_types,
                                                                                           'property': property})
    if request.method == 'POST':
        house.delete()
        messages.success(request, 'Suppression effectuée !')
        return redirect('property_management_part1', property_pk=property_pk)


#####################################################end house#################################################


#################################################room###############################
@login_required
def edit_room(request, property_pk, room_pk):
    property = get_object_or_404(Property, pk=property_pk)
    room = get_object_or_404(Room, pk=room_pk)
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        form = Studio_Form(instance=room)
        return render(request, 'real_estate/property_management/room/edit_room.html', {'room': room,
                                                                                       'form': form, 'service_types':
                                                                                           service_types,
                                                                                       'property': property})
    else:
        try:
            form = Room_Form(request.POST, instance=room)
            form = form.save(commit=False)
            form.property = get_object_or_404(Property, id=property_pk)
            form.save()
            messages.success(request, 'Modification éffectuée !')
            return redirect('property_management_part1', property_pk=property_pk)
        except ValueError:
            return render(request, 'real_estate/property_management/room/edit_room.html',
                          {'room': room, 'form': form,
                           'property': property, 'service_types': service_types,
                           'error': 'Mauvaises données saisies !'})


@login_required
def clone_room(request, property_pk, room_pk):
    property = get_object_or_404(Property, pk=property_pk)
    room = get_object_or_404(Room, pk=room_pk)
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        form = Studio_Form(instance=room)
        return render(request, 'real_estate/property_management/room/clone_room.html', {'room': room,
                                                                                        'form': form, 'service_types':
                                                                                            service_types,
                                                                                        'property': property})
    else:
        try:
            form = Room_Form(request.POST)
            form = form.save(commit=False)
            form.property = get_object_or_404(Property, id=property_pk)
            form.save()
            messages.success(request, 'Modification éffectuée !')
            return redirect('property_management_part1', property_pk=property_pk)
        except ValueError:
            return render(request, 'real_estate/property_management/room/clone_room.html',
                          {'room': room, 'form': form,
                           'property': property, 'service_types': service_types,
                           'error': 'Mauvaises données saisies !'})


@login_required
def delete_room(request, property_pk, room_pk):
    property = get_object_or_404(Property, pk=property_pk)
    room = get_object_or_404(Room, pk=room_pk)
    service_types = Service_Type.objects.all()

    if request.method == 'GET':
        form = Studio_Form(instance=room)
        return render(request, 'real_estate/property_management/room/delete_room.html', {'room': room,
                                                                                         'form': form, 'service_types':
                                                                                             service_types,
                                                                                         'property': property})
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Suppression effectuée !')
        return redirect('property_management_part1', property_pk=property_pk)


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
            if get_object_or_404(Cart, land_id=request.POST.get('land_id')):
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
def property_management_ad_detail(request, property_pk, object_pk):
    property = get_object_or_404(Property, pk=property_pk)
    apartment = Apartment.objects.filter(id=object_pk)
    studio = Studio.objects.filter(id=object_pk)
    house = House.objects.filter(id=object_pk)
    room = Room.objects.filter(id=object_pk)
    apartment_images = Apartment_Image.objects.filter(apartment_id=object_pk)
    studio_images = Studio_Image.objects.filter(studio_id=object_pk)
    house_images = House_Image.objects.filter(house_id=object_pk)
    room_images = Room_Image.objects.filter(room_id=object_pk)
    service_types = Service_Type.objects.all()
    cart_count = Cart.objects.filter(user=request.user)
    property_types = Property_Type.objects.all()

    if request.method == 'GET':
        form = Cart_Form()
        return render(request, 'real_estate/property_management/property_management_ad_detail.html',
                      {'property': property, 'apartment': apartment, 'studio': studio, 'house': house, 'room': room,
                       'apartment_images': apartment_images, 'studio_images': studio_images,
                       'house_images': house_images
                          , 'room_images': room_images, 'form': form, 'cart_count': cart_count, 'service_types':
                           service_types, 'property_types': property_types})
    else:
        try:
            form = Cart_Form(request.POST)
            if get_object_or_404(Cart, land_id=request.POST.get('land_id')):
                messages.error(request, 'Erreur ! Ce terrain existe déjà dans votre panier !')
                return redirect('land_project')
            else:
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                messages.success(request, 'Ajout au panier éffectué !')
                return redirect('land_project')
        except ValueError:
            return render(request, 'real_estate/property_management/property_management_ad_detail.html',
                          {'property': property, 'apartment': apartment, 'studio': studio, 'house': house, 'room': room,
                           'apartment_images': apartment_images, 'studio_images': studio_images,
                           'house_images': house_images
                              , 'room_images': room_images, 'form': form, 'cart_count': cart_count, 'service_types':
                               service_types, 'property_types': property_types,
                           'error': 'Mauvaises données saisies !'})