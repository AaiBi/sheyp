from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from construction.forms import Construction_floor_Form, Devis_Form
from construction.models import Construction_Project, Construction_Type, Construction_floor, Country, Quote_Project, \
    Quote_Project_Step, Mesure_Unit, Quote_Project_Ouvrage, Materiaux, Quote_Project_Materiaux


def construction(request):
    if request.method == 'POST':
        if 'construction_project_submit' in request.POST:
            if request.user.is_authenticated:
                return redirect('construction_part1')
            else:
                messages.error(request, 'Veuillez vous connectez pour pouvoir commencer un projet de construction !')
                return redirect('login_user')

    return render(request, 'construction/construction.html')


def construction_part1(request):
    construction_types = Construction_Type.objects.all()

    if request.method == 'GET':
        return render(request, 'construction/construction_part1.html', {'construction_types': construction_types})
    else:
        try:
            client_first_name = request.POST.get('client_first_name')
            client_last_name = request.POST.get('client_last_name')
            client_email = request.POST.get('client_email')
            client_phone_number = request.POST.get('client_phone_number')

            messages.success(request, 'Phase 1 terminée !')
            return redirect('construction_part2', client_first_name=client_first_name, client_last_name=client_last_name
                            , client_email=client_email, client_phone_number=client_phone_number)

        except ValueError:
            return render(request, 'construction/construction_part1.html', {'construction_types': construction_types,
                                                                            'error': 'Mauvaises données saisies !'})


def construction_part2(request, client_first_name, client_last_name, client_email, client_phone_number):
    construction_types = Construction_Type.objects.all()

    if request.method == 'GET':
        return render(request, 'construction/construction_part2.html', {'construction_types': construction_types,
                                                                        'client_first_name': client_first_name,
                                                                        'client_last_name': client_last_name,
                                                                        'client_email': client_email,
                                                                        'client_phone_number': client_phone_number})
    else:
        try:
            construction_type_id = request.POST.get('construction_type_id')
            region = request.POST.get('region')
            adress = request.POST.get('adress')
            area = request.POST.get('area')
            area_usable = request.POST.get('area_usable')
            number_floor = request.POST.get('number_floor')
            aditionnal_info = request.POST.get('aditionnal_info')

            construction_project = Construction_Project(region=region, adress=adress, area=area, area_usable=
            area_usable, aditionnal_info=aditionnal_info, number_floor=
                                                        number_floor, client_first_name=client_first_name,
                                                        client_last_name=client_last_name, client_email=client_email
                                                        , client_phone_number=client_phone_number, construction_type_id
                                                        =construction_type_id)
            construction_project.save()

            messages.success(request, 'Phase 2 terminée !')
            return redirect('construction_part3', construction_project_pk=construction_project.id)

        except ValueError:
            return render(request, 'construction/construction_part2.html',
                          {'construction_types': construction_types, 'error': 'Mauvaises données saisies !'})


def construction_part3(request, construction_project_pk):
    construction_project = Construction_Project.objects.filter(pk=construction_project_pk).last()
    number_construction_floor = Construction_floor.objects.filter(construction_project_id=construction_project_pk) \
        .count()
    construction_floors = Construction_floor.objects.filter(construction_project_id=construction_project_pk)
    total_floors = construction_project.number_floor + 1
    if 'complete_construction_project_info' in request.POST:
        if request.method == 'POST':
            messages.success(request, 'Votre demande a été envoyer avec succès, nous vous contacterons très bientôt !')
            return redirect('construction')

    if request.method == 'GET':
        construction_floor_form = Construction_floor_Form()
        return render(request, 'construction/construction_part3.html', {'construction_project': construction_project,
                                                                        'construction_floor_form':
                                                                            construction_floor_form,
                                                                        'number_construction_floor':
                                                                            number_construction_floor,
                                                                        'construction_floors': construction_floors,
                                                                        'total_floors': total_floors
                                                                        })
    else:
        try:
            # construction_floor_form = Architecture_Image_Form(request.POST, request.FILES)
            construction_floor_form = Construction_floor_Form(request.POST)
            if construction_floor_form.is_valid():
                # Saving the land infos for the consruction project#
                construction_floor_form = construction_floor_form.save(commit=False)
                construction_floor_form.construction_project = get_object_or_404(Construction_Project,
                                                                                 id=construction_project.id)
                construction_floor_form.save()
                messages.success(request, 'Informations enregistrées avec succès !')
                return redirect('construction_part3', construction_project_pk=construction_project_pk)

        except ValueError:
            return render(request, 'construction/construction_part3.html', {'construction_project': construction_project
                , 'construction_floors': construction_floors
                , 'total_floors': total_floors
                , 'error': 'Mauvaises données saisies !'})


# ###################################### Automatic quote ##################################################
# ###################################### Automatic quote ##################################################


def automatic_quote(request):
    countries = Country.objects.all()
    devis_form = Devis_Form()

    if request.method == 'POST':
        devis_form = Devis_Form(request.POST)
        if devis_form.is_valid():
            devis_form = devis_form.save(commit=False)
            if request.POST.get('country_id') == "":
                messages.error(request, 'Veillez selectionner votre pays de residence !')
            else:
                devis_form.country = get_object_or_404(Country, id=request.POST.get('country'))
                devis_form.save()
                return redirect('automatic_quote_result', quote_pk=devis_form.id)
        else:
            messages.error(request, 'Le formulaire est invalide, mauvaises données saisies !')

    return render(request, 'construction/automatic quote/automatic_quote.html', {
        'countries': countries, 'devis_form': devis_form
    })


def automatic_quote_result(request, quote_pk):
    quote_project = get_object_or_404(Quote_Project, pk=quote_pk)
    if quote_project.level > 1:
        house_level = quote_project.level - 1
    else:
        house_level = quote_project.level
    countries = Country.objects.all()
    mesure_units = Mesure_Unit.objects.all()
    materiaux = Materiaux.objects.all()
    quote_project_steps = Quote_Project_Step.objects.all()

    # ############ List of the ouvrages for the Fondation step #############

    # Mur de soubassement #
    mur_soubassement = Quote_Project_Ouvrage.objects.filter(
        name="Mur de soubassement", quote_project_step__name="Fondation"
    ).last()
    mur_soubassement_quantity = round(float(mur_soubassement.quantity * quote_project.area) / 3.5, 4)
    quote_project_materiaux_fondation_mur_soubassement = Quote_Project_Materiaux.objects.filter(
        quote_project_ouvrage__name="Mur de soubassement"
    )
    mur_soubassement_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Mur de soubassement"
    ).last()
    mur_soubassement_ciment_quantity = round(float(mur_soubassement_ciment.quantity * quote_project.area) / 3.5, 4)

    mur_soubassement_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Mur de soubassement"
    ).last()
    mur_soubassement_sable_quantity = round(float(mur_soubassement_sable.quantity * quote_project.area) / 3.5, 4)

    mur_soubassement_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Mur de soubassement"
    ).last()
    mur_soubassement_gravier_quantity = round(float(mur_soubassement_gravier.quantity * quote_project.area) / 3.5, 4)

    mur_soubassement_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Mur de soubassement"
    ).last()
    mur_soubassement_eau_quantity = round(float(mur_soubassement_eau.quantity * quote_project.area) / 3.5, 4)

    mur_soubassement_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Mur de soubassement"
    ).last()
    mur_soubassement_acier_quantity = round(float(mur_soubassement_acier.quantity * quote_project.area) / 3.5, 4)
    # End Mur de soubassement #

    # Béton de propreté #
    beton_proprete = Quote_Project_Ouvrage.objects.filter(
        name="Béton de propreté", quote_project_step__name="Fondation"
    ).last()
    beton_proprete_quantity = round(float(beton_proprete.quantity * quote_project.area) / 3.5, 4)
    quote_project_materiaux_fondation_beton_proprete = Quote_Project_Materiaux.objects.filter(
        quote_project_ouvrage__name="Béton de propreté"
    )
    beton_proprete_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Béton de propreté"
    ).last()
    beton_proprete_ciment_quantity = round(float(beton_proprete_ciment.quantity * quote_project.area) / 3.5, 4)

    beton_proprete_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Béton de propreté"
    ).last()
    beton_proprete_sable_quantity = round(float(beton_proprete_sable.quantity * quote_project.area) / 3.5, 4)

    beton_proprete_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Béton de propreté"
    ).last()
    beton_proprete_gravier_quantity = round(float(beton_proprete_gravier.quantity * quote_project.area) / 3.5, 4)

    beton_proprete_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Béton de propreté"
    ).last()
    beton_proprete_eau_quantity = round(float(beton_proprete_eau.quantity * quote_project.area) / 3.5, 4)

    beton_proprete_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Béton de propreté"
    ).last()
    beton_proprete_acier_quantity = round(float(beton_proprete_acier.quantity * quote_project.area) / 3.5, 4)
    # End Béton de propreté #

    # Semelles #
    semelles = Quote_Project_Ouvrage.objects.filter(
        name="Semelles", quote_project_step__name="Fondation"
    ).last()
    semelles_quantity = round(float(semelles.quantity * quote_project.area) / 3.5, 4)
    quote_project_materiaux_fondation_semelles = Quote_Project_Materiaux.objects.filter(
        quote_project_ouvrage__name="Semelles"
    )
    semelles_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Semelles"
    ).last()
    semelles_ciment_quantity = round(float(semelles_ciment.quantity * quote_project.area) / 3.5, 4)

    semelles_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Semelles"
    ).last()
    semelles_sable_quantity = round(float(semelles_sable.quantity * quote_project.area) / 3.5, 4)

    semelles_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Semelles"
    ).last()
    semelles_gravier_quantity = round(float(semelles_gravier.quantity * quote_project.area) / 3.5, 4)

    semelles_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Semelles"
    ).last()
    semelles_eau_quantity = round(float(semelles_eau.quantity * quote_project.area) / 3.5, 4)

    semelles_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Semelles"
    ).last()
    semelles_acier_quantity = round(float(semelles_acier.quantity * quote_project.area) / 3.5, 4)
    # End Semelles #

    # Amorces poteaux #
    amorces_poteaux = Quote_Project_Ouvrage.objects.filter(
        name="Amorces poteaux", quote_project_step__name="Fondation"
    ).last()
    amorces_poteaux_quantity = round(float(amorces_poteaux.quantity * quote_project.area) / 3.5, 4)
    quote_project_materiaux_fondation_amorces_poteaux = Quote_Project_Materiaux.objects.filter(
        quote_project_ouvrage__name="Amorces poteaux"
    )
    amorces_poteaux_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Amorces poteaux"
    ).last()
    amorces_poteaux_ciment_quantity = round(float(amorces_poteaux_ciment.quantity * quote_project.area) / 3.5, 4)

    amorces_poteaux_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Amorces poteaux"
    ).last()
    amorces_poteaux_sable_quantity = round(float(amorces_poteaux_sable.quantity * quote_project.area) / 3.5, 4)

    amorces_poteaux_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Amorces poteaux"
    ).last()
    amorces_poteaux_gravier_quantity = round(float(amorces_poteaux_gravier.quantity * quote_project.area) / 3.5, 4)

    amorces_poteaux_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Amorces poteaux"
    ).last()
    amorces_poteaux_eau_quantity = round(float(amorces_poteaux_eau.quantity * quote_project.area) / 3.5, 4)

    amorces_poteaux_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Amorces poteaux"
    ).last()
    amorces_poteaux_acier_quantity = round(float(amorces_poteaux_acier.quantity * quote_project.area) / 3.5, 4)
    # End Amorces poteaux #

    # Longrines #
    longrines = Quote_Project_Ouvrage.objects.filter(
        name="Longrines", quote_project_step__name="Fondation"
    ).last()
    longrines_quantity = round(float(longrines.quantity * quote_project.area) / 3.5, 4)
    quote_project_materiaux_fondation_longrines = Quote_Project_Materiaux.objects.filter(
        quote_project_ouvrage__name="Longrines"
    )
    longrines_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Longrines"
    ).last()
    longrines_ciment_quantity = round(float(longrines_ciment.quantity * quote_project.area) / 3.5, 4)

    longrines_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Longrines"
    ).last()
    longrines_sable_quantity = round(float(longrines_sable.quantity * quote_project.area) / 3.5, 4)

    longrines_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Longrines"
    ).last()
    longrines_gravier_quantity = round(float(longrines_gravier.quantity * quote_project.area) / 3.5, 4)

    longrines_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Longrines"
    ).last()
    longrines_eau_quantity = round(float(longrines_eau.quantity * quote_project.area) / 3.5, 4)

    longrines_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Longrines"
    ).last()
    longrines_acier_quantity = round(float(longrines_acier.quantity * quote_project.area) / 3.5, 4)
    # End Longrines #

    # Remblais #
    remblais = Quote_Project_Ouvrage.objects.filter(
        name="Remblais", quote_project_step__name="Fondation"
    ).last()
    remblais_quantity = round(float(remblais.quantity * quote_project.area) / 3.5, 4)
    quote_project_materiaux_fondation_remblais = Quote_Project_Materiaux.objects.filter(
        quote_project_ouvrage__name="Remblais"
    )
    remblais_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Remblais"
    ).last()
    remblais_ciment_quantity = round(float(remblais_ciment.quantity * quote_project.area) / 3.5, 4)

    remblais_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Remblais"
    ).last()
    remblais_sable_quantity = round(float(remblais_sable.quantity * quote_project.area) / 3.5, 4)

    remblais_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Remblais"
    ).last()
    remblais_gravier_quantity = round(float(remblais_gravier.quantity * quote_project.area) / 3.5, 4)

    remblais_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Remblais"
    ).last()
    remblais_eau_quantity = round(float(remblais_eau.quantity * quote_project.area) / 3.5, 4)

    remblais_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Remblais"
    ).last()
    remblais_acier_quantity = round(float(remblais_acier.quantity * quote_project.area) / 3.5, 4)
    # End Remblais #

    # Total fondation #
    total_quantity_ciment = round(
        mur_soubassement_ciment_quantity + beton_proprete_ciment_quantity + semelles_ciment_quantity +
        amorces_poteaux_ciment_quantity + longrines_ciment_quantity + remblais_ciment_quantity, 4
    )
    total_quantity_ciment_int = int(total_quantity_ciment)
    if total_quantity_ciment_int == 0:
        total_quantity_ciment_int = round(total_quantity_ciment, 1)

    total_quantity_sable = round(
        mur_soubassement_sable_quantity + beton_proprete_sable_quantity + semelles_sable_quantity +
        amorces_poteaux_sable_quantity + longrines_sable_quantity + remblais_sable_quantity, 4
    )
    total_quantity_sable_int = int(total_quantity_sable)
    if total_quantity_sable_int == 0:
        total_quantity_sable_int = round(total_quantity_sable, 1)

    total_quantity_gravier = round(
        mur_soubassement_gravier_quantity + beton_proprete_gravier_quantity + semelles_gravier_quantity +
        amorces_poteaux_gravier_quantity + longrines_gravier_quantity + remblais_gravier_quantity, 4
    )
    total_quantity_gravier_int = int(total_quantity_gravier)
    if total_quantity_gravier_int == 0:
        total_quantity_gravier_int = round(total_quantity_gravier, 1)

    total_quantity_eau = round(
        mur_soubassement_eau_quantity + beton_proprete_eau_quantity + semelles_eau_quantity +
        amorces_poteaux_eau_quantity + longrines_eau_quantity + remblais_eau_quantity, 4
    )

    total_quantity_acier = round(
        mur_soubassement_acier_quantity + beton_proprete_acier_quantity + semelles_acier_quantity +
        amorces_poteaux_acier_quantity + longrines_acier_quantity + remblais_acier_quantity, 4
    )
    total_quantity_acier_int = int(total_quantity_acier)
    if total_quantity_acier_int == 0:
        total_quantity_acier_int = round(total_quantity_acier, 1)
    # End total fondation #

    # ############ End List of the ouvrages for the Fondation step #############

    # ############ List of the ouvrages for the Elevation step #################
    # Maçonnerie #
    maconnerie = Quote_Project_Ouvrage.objects.filter(
        name="Maçonnerie", quote_project_step__name="Élévation"
    ).last()
    maconnerie_quantity = round(float(maconnerie.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    maconnerie_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Maçonnerie"
    ).first()
    maconnerie_ciment_quantity = round(float(maconnerie_ciment.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    maconnerie_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Maçonnerie"
    ).first()
    maconnerie_sable_quantity = round(float(maconnerie_sable.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    maconnerie_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Maçonnerie"
    ).first()
    maconnerie_gravier_quantity = round(float(maconnerie_gravier.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    maconnerie_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Maçonnerie"
    ).first()
    maconnerie_eau_quantity = round(float(maconnerie_eau.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    maconnerie_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Maçonnerie"
    ).first()
    maconnerie_acier_quantity = round(float(maconnerie_acier.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    # End Maçonnerie #

    # Linteaux #
    linteaux = Quote_Project_Ouvrage.objects.filter(
        name="Linteaux", quote_project_step__name="Élévation"
    ).last()
    linteaux_quantity = round(float(linteaux.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    linteaux_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Linteaux"
    ).last()
    linteaux_ciment_quantity = round(float(linteaux_ciment.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    linteaux_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Linteaux"
    ).last()
    linteaux_sable_quantity = round(float(linteaux_sable.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    linteaux_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Linteaux"
    ).last()
    linteaux_gravier_quantity = round(float(linteaux_gravier.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    linteaux_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Linteaux"
    ).last()
    linteaux_eau_quantity = round(float(linteaux_eau.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    linteaux_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Linteaux"
    ).last()
    linteaux_acier_quantity = round(float(linteaux_acier.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    # End Linteaux #

    # Poutre #
    poutre = Quote_Project_Ouvrage.objects.filter(
        name="Poutre", quote_project_step__name="Élévation"
    ).last()
    poutre_quantity = round(float(poutre.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    poutre_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Poutre"
    ).last()
    poutre_ciment_quantity = round(float(poutre_ciment.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    poutre_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Poutre"
    ).last()
    poutre_sable_quantity = round(float(poutre_sable.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    poutre_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Poutre"
    ).last()
    poutre_gravier_quantity = round(float(poutre_gravier.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    poutre_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Poutre"
    ).last()
    poutre_eau_quantity = round(float(poutre_eau.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    poutre_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Poutre"
    ).last()
    poutre_acier_quantity = round(float(poutre_acier.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    # End Poutre #

    # Coulage #
    coulage = Quote_Project_Ouvrage.objects.filter(
        name="Coulage", quote_project_step__name="Élévation"
    ).last()
    coulage_quantity = round(float(coulage.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    coulage_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Coulage"
    ).last()
    coulage_ciment_quantity = round(float(coulage_ciment.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    coulage_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Coulage"
    ).last()
    coulage_sable_quantity = round(float(coulage_sable.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    coulage_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Coulage"
    ).last()
    coulage_gravier_quantity = round(float(coulage_gravier.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    coulage_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Coulage"
    ).last()
    coulage_eau_quantity = round(float(coulage_eau.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    coulage_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Coulage"
    ).last()
    coulage_acier_quantity = round(float(coulage_acier.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    # End Coulage #

    # Mortier #
    mortier = Quote_Project_Ouvrage.objects.filter(
        name="Mortier", quote_project_step__name="Élévation"
    ).last()
    mortier_quantity = round(float(mortier.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    mortier_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Mortier"
    ).first()
    mortier_ciment_quantity = round(float(mortier_ciment.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    mortier_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Mortier"
    ).first()
    mortier_sable_quantity = round(float(mortier_sable.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    mortier_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Mortier"
    ).first()
    mortier_gravier_quantity = round(float(mortier_gravier.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    mortier_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Mortier"
    ).first()
    mortier_eau_quantity = round(float(mortier_eau.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    mortier_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Mortier"
    ).first()
    mortier_acier_quantity = round(float(mortier_acier.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    # End Mortier #

    # Enduits Interieur #
    enduits_interieur = Quote_Project_Ouvrage.objects.filter(
        name="Enduits Interieur", quote_project_step__name="Élévation"
    ).last()
    enduits_interieur_quantity = round(float(enduits_interieur.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    enduits_interieur_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Enduits Interieur"
    ).first()
    enduits_interieur_ciment_quantity = round(float(enduits_interieur_ciment.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    enduits_interieur_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Enduits Interieur"
    ).first()
    enduits_interieur_sable_quantity = round(float(enduits_interieur_sable.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    enduits_interieur_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Enduits Interieur"
    ).first()
    enduits_interieur_gravier_quantity = round(float(enduits_interieur_gravier.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    enduits_interieur_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Enduits Interieur"
    ).first()
    enduits_interieur_eau_quantity = round(float(enduits_interieur_eau.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    enduits_interieur_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Enduits Interieur"
    ).first()
    enduits_interieur_acier_quantity = round(float(enduits_interieur_acier.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    # End Enduits Interieur #

    # Enduits sous plafond #
    enduits_sous_plafond = Quote_Project_Ouvrage.objects.filter(
        name="Enduits sous plafond", quote_project_step__name="Élévation"
    ).last()
    enduits_sous_plafond_quantity = round(float(enduits_sous_plafond.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    enduits_sous_plafond_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Enduits sous plafond"
    ).first()
    enduits_sous_plafond_ciment_quantity = round(float(enduits_sous_plafond_ciment.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    enduits_sous_plafond_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Enduits sous plafond"
    ).first()
    enduits_sous_plafond_sable_quantity = round(float(
        enduits_sous_plafond_sable.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    enduits_sous_plafond_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Enduits sous plafond"
    ).first()
    enduits_sous_plafond_gravier_quantity = round(float(
        enduits_sous_plafond_gravier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    enduits_sous_plafond_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Enduits sous plafond"
    ).first()
    enduits_sous_plafond_eau_quantity = round(float(enduits_sous_plafond_eau.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    enduits_sous_plafond_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Enduits sous plafond"
    ).first()
    enduits_sous_plafond_acier_quantity = round(float(
        enduits_sous_plafond_acier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    # Enduits sous plafond #

    # Enduits Exterieur #
    enduits_exterieur = Quote_Project_Ouvrage.objects.filter(
        name="Enduits Exterieur", quote_project_step__name="Élévation"
    ).last()
    enduits_exterieur_quantity = round(float(enduits_exterieur.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    enduits_exterieur_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Enduits Exterieur"
    ).first()
    enduits_exterieur_ciment_quantity = round(float(enduits_exterieur_ciment.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    enduits_exterieur_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Enduits Exterieur"
    ).first()
    enduits_exterieur_sable_quantity = round(float(enduits_exterieur_sable.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    enduits_exterieur_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Enduits Exterieur"
    ).first()
    enduits_exterieur_gravier_quantity = round(float(enduits_exterieur_gravier.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    enduits_exterieur_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Enduits Exterieur"
    ).first()
    enduits_exterieur_eau_quantity = round(float(enduits_exterieur_eau.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    enduits_exterieur_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Enduits Exterieur"
    ).first()
    enduits_exterieur_acier_quantity = round(float(enduits_exterieur_acier.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    # Enduits Exterieur #

    # Poteaux #
    poteaux = Quote_Project_Ouvrage.objects.filter(
        name="Poteaux", quote_project_step__name="Élévation"
    ).last()
    poteaux_quantity = round(float(poteaux.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    poteaux_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Poteaux"
    ).first()
    poteaux_ciment_quantity = round(float(poteaux_ciment.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    poteaux_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Poteaux"
    ).first()
    poteaux_sable_quantity = round(float(poteaux_sable.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    poteaux_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Poteaux"
    ).first()
    poteaux_gravier_quantity = round(float(poteaux_gravier.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    poteaux_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Poteaux"
    ).first()
    poteaux_eau_quantity = round(float(poteaux_eau.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    poteaux_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Poteaux"
    ).first()
    poteaux_acier_quantity = round(float(poteaux_acier.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    # Poteaux #

    # Escalier #
    escalier = Quote_Project_Ouvrage.objects.filter(
        name="Escalier", quote_project_step__name="Élévation"
    ).last()
    escalier_quantity = round(float(escalier.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    escalier_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Escalier"
    ).last()
    escalier_ciment_quantity = round(float(escalier_ciment.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    escalier_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Escalier"
    ).last()
    escalier_sable_quantity = round(float(escalier_sable.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    escalier_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Escalier"
    ).last()
    escalier_gravier_quantity = round(float(escalier_gravier.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    escalier_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Escalier"
    ).last()
    escalier_eau_quantity = round(float(escalier_eau.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    escalier_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Escalier"
    ).last()
    escalier_acier_quantity = round(float(escalier_acier.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    # End Escalier #

    # Dallage sol #
    dallage_sol = Quote_Project_Ouvrage.objects.filter(
        name="Dallage sol", quote_project_step__name="Élévation"
    ).last()
    dallage_sol_quantity = round(float(dallage_sol.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    dallage_sol_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Dallage sol"
    ).last()
    dallage_sol_ciment_quantity = round(float(dallage_sol_ciment.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    dallage_sol_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Dallage sol"
    ).last()
    dallage_sol_sable_quantity = round(float(dallage_sol_sable.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    dallage_sol_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Dallage sol"
    ).last()
    dallage_sol_gravier_quantity = round(float(dallage_sol_gravier.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    dallage_sol_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Dallage sol"
    ).last()
    dallage_sol_eau_quantity = round(float(dallage_sol_eau.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    dallage_sol_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Dallage sol"
    ).last()
    dallage_sol_acier_quantity = round(float(dallage_sol_acier.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    # End Dallage sol #

    # Fosse sceptique #
    fosse_sceptique = Quote_Project_Ouvrage.objects.filter(
        name="Fosse sceptique", quote_project_step__name="Élévation"
    ).last()
    fosse_sceptique_quantity = round(float(fosse_sceptique.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    fosse_sceptique_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Fosse sceptique"
    ).last()
    fosse_sceptique_ciment_quantity = round(float(fosse_sceptique_ciment.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    fosse_sceptique_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Fosse sceptique"
    ).last()
    fosse_sceptique_sable_quantity = round(float(fosse_sceptique_sable.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    fosse_sceptique_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Fosse sceptique"
    ).last()
    fosse_sceptique_gravier_quantity = round(float(fosse_sceptique_gravier.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    fosse_sceptique_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Fosse sceptique"
    ).last()
    fosse_sceptique_eau_quantity = round(float(fosse_sceptique_eau.quantity * quote_project.area) / 3.5, 4) * quote_project.level

    fosse_sceptique_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Fosse sceptique"
    ).last()
    fosse_sceptique_acier_quantity = round(float(fosse_sceptique_acier.quantity * quote_project.area) / 3.5, 4) * quote_project.level
    # End Fosse sceptique #

    # Total elevation #
    total_quantity_ciment_elevation = round(
        maconnerie_ciment_quantity + linteaux_ciment_quantity + poutre_ciment_quantity + coulage_ciment_quantity +
        mortier_ciment_quantity + enduits_interieur_ciment_quantity + enduits_sous_plafond_ciment_quantity +
        enduits_exterieur_ciment_quantity + poteaux_ciment_quantity + escalier_ciment_quantity +
        dallage_sol_ciment_quantity + fosse_sceptique_ciment_quantity, 4
    )
    total_quantity_ciment_elevation_int = int(total_quantity_ciment_elevation)
    if total_quantity_ciment_elevation_int == 0:
        total_quantity_ciment_elevation_int = round(total_quantity_ciment_elevation, 1)

    total_quantity_sable_elevation = round(
        maconnerie_sable_quantity + linteaux_sable_quantity + poutre_sable_quantity + coulage_sable_quantity +
        mortier_sable_quantity + enduits_interieur_sable_quantity + enduits_sous_plafond_sable_quantity +
        enduits_exterieur_sable_quantity + poteaux_sable_quantity + escalier_sable_quantity +
        dallage_sol_sable_quantity + fosse_sceptique_sable_quantity, 4
    )
    total_quantity_sable_elevation_int = int(total_quantity_sable_elevation)
    if total_quantity_sable_elevation_int == 0:
        total_quantity_sable_elevation_int = round(total_quantity_sable_elevation, 1)

    total_quantity_gravier_elevation = round(
        maconnerie_gravier_quantity + linteaux_gravier_quantity + poutre_gravier_quantity + coulage_gravier_quantity +
        mortier_gravier_quantity + enduits_interieur_gravier_quantity + enduits_sous_plafond_gravier_quantity +
        enduits_exterieur_gravier_quantity + poteaux_gravier_quantity + escalier_gravier_quantity +
        dallage_sol_gravier_quantity + fosse_sceptique_gravier_quantity, 4
    )
    total_quantity_gravier_elevation_int = int(total_quantity_gravier_elevation)
    if total_quantity_gravier_elevation_int == 0:
        total_quantity_gravier_elevation_int = round(total_quantity_gravier_elevation, 1)

    total_quantity_eau_elevation = round(
        maconnerie_eau_quantity + linteaux_eau_quantity + poutre_eau_quantity + coulage_eau_quantity +
        mortier_eau_quantity + enduits_interieur_eau_quantity + enduits_sous_plafond_eau_quantity +
        enduits_exterieur_eau_quantity + poteaux_eau_quantity + escalier_eau_quantity + dallage_sol_eau_quantity +
        fosse_sceptique_eau_quantity, 4
    )

    total_quantity_acier_elevation = round(
        maconnerie_acier_quantity + linteaux_acier_quantity + poutre_acier_quantity + coulage_acier_quantity +
        mortier_acier_quantity + enduits_interieur_acier_quantity + enduits_sous_plafond_acier_quantity +
        enduits_exterieur_acier_quantity + poteaux_acier_quantity + escalier_acier_quantity + dallage_sol_acier_quantity
        + fosse_sceptique_acier_quantity, 4
    )
    total_quantity_acier_elevation_int = int(total_quantity_acier_elevation)
    if total_quantity_acier_elevation_int == 0:
        total_quantity_acier_elevation_int = round(total_quantity_acier_elevation, 1)
    # End total elevation #

    # ############ End List of the ouvrages for the Elevation step #############

    # ############ End List of the ouvrages for the Terrasse step #############
    # Maçonnerie #
    maconnerie_terrasse = Quote_Project_Ouvrage.objects.filter(
        name="Maçonnerie", quote_project_step__name="Terrasse"
    ).last()
    maconnerie_terrasse_quantity = round(
        float(maconnerie_terrasse.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    maconnerie_terrasse_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Maçonnerie"
    ).last()
    maconnerie_terrasse_ciment_quantity = round(float(maconnerie_terrasse_ciment.quantity * quote_project.area) / 3.5,
                                       4) * quote_project.level

    maconnerie_terrasse_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Maçonnerie"
    ).last()
    maconnerie_terrasse_sable_quantity = round(float(maconnerie_terrasse_sable.quantity * quote_project.area) / 3.5,
                                      4) * quote_project.level

    maconnerie_terrasse_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Maçonnerie"
    ).last()
    maconnerie_terrasse_gravier_quantity = round(float(maconnerie_terrasse_gravier.quantity * quote_project.area) / 3.5,
                                        4) * quote_project.level

    maconnerie_terrasse_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Maçonnerie"
    ).last()
    maconnerie_terrasse_eau_quantity = round(
        float(maconnerie_terrasse_eau.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    maconnerie_terrasse_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Maçonnerie"
    ).last()
    maconnerie_terrasse_acier_quantity = round(
        float(maconnerie_terrasse_acier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    # End Maçonnerie #

    # Coulage cage escalier #
    coulage_cage_escalier_terrasse = Quote_Project_Ouvrage.objects.filter(
        name="Coulage cage escalier", quote_project_step__name="Terrasse"
    ).last()
    coulage_cage_escalier_terrasse_quantity = round(
        float(coulage_cage_escalier_terrasse.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    coulage_cage_escalier_terrasse_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Coulage cage escalier"
    ).last()
    coulage_cage_escalier_terrasse_ciment_quantity = round(
        float(coulage_cage_escalier_terrasse_ciment.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    coulage_cage_escalier_terrasse_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Coulage cage escalier"
    ).last()
    coulage_cage_escalier_terrasse_sable_quantity = round(
        float(coulage_cage_escalier_terrasse_sable.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    coulage_cage_escalier_terrasse_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Coulage cage escalier"
    ).last()
    coulage_cage_escalier_terrasse_gravier_quantity = round(
        float(coulage_cage_escalier_terrasse_gravier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    coulage_cage_escalier_terrasse_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Coulage cage escalier"
    ).last()
    coulage_cage_escalier_terrasse_eau_quantity = round(
        float(coulage_cage_escalier_terrasse_eau.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    coulage_cage_escalier_terrasse_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Coulage cage escalier"
    ).last()
    coulage_cage_escalier_terrasse_acier_quantity = round(
        float(coulage_cage_escalier_terrasse_acier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    # End Coulage cage escalier #

    # Mortier #
    mortier_terrasse = Quote_Project_Ouvrage.objects.filter(
        name="Mortier", quote_project_step__name="Terrasse"
    ).last()
    mortier_terrasse_quantity = round(
        float(mortier_terrasse.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    mortier_terrasse_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Mortier"
    ).last()
    mortier_terrasse_ciment_quantity = round(
        float(mortier_terrasse_ciment.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    mortier_terrasse_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Mortier"
    ).last()
    mortier_terrasse_sable_quantity = round(
        float(mortier_terrasse_sable.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    mortier_terrasse_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Mortier"
    ).last()
    mortier_terrasse_gravier_quantity = round(
        float(mortier_terrasse_gravier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    mortier_terrasse_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Mortier"
    ).last()
    mortier_terrasse_eau_quantity = round(
        float(mortier_terrasse_eau.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    mortier_terrasse_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Mortier"
    ).last()
    mortier_terrasse_acier_quantity = round(
        float(mortier_terrasse_acier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    # End Mortier #

    # Enduits Interieur #
    enduits_interieur_terrasse = Quote_Project_Ouvrage.objects.filter(
        name="Enduits Interieur", quote_project_step__name="Terrasse"
    ).last()
    enduits_interieur_terrasse_quantity = round(
        float(enduits_interieur_terrasse.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    enduits_interieur_terrasse_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Enduits Interieur"
    ).last()
    enduits_interieur_terrasse_ciment_quantity = round(
        float(enduits_interieur_terrasse_ciment.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    enduits_interieur_terrasse_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Enduits Interieur"
    ).last()
    enduits_interieur_terrasse_sable_quantity = round(
        float(enduits_interieur_terrasse_sable.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    enduits_interieur_terrasse_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Enduits Interieur"
    ).last()
    enduits_interieur_terrasse_gravier_quantity = round(
        float(enduits_interieur_terrasse_gravier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    enduits_interieur_terrasse_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Enduits Interieur"
    ).last()
    enduits_interieur_terrasse_eau_quantity = round(
        float(enduits_interieur_terrasse_eau.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    enduits_interieur_terrasse_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Enduits Interieur"
    ).last()
    enduits_interieur_terrasse_acier_quantity = round(
        float(enduits_interieur_terrasse_acier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    # End Enduits Interieur #

    # Enduits sous plafond #
    enduits_sous_plafond_terrasse = Quote_Project_Ouvrage.objects.filter(
        name="Enduits sous plafond", quote_project_step__name="Terrasse"
    ).last()
    enduits_sous_plafond_terrasse_quantity = round(
        float(enduits_sous_plafond_terrasse.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    enduits_sous_plafond_terrasse_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Enduits sous plafond"
    ).last()
    enduits_sous_plafond_terrasse_ciment_quantity = round(
        float(enduits_sous_plafond_terrasse_ciment.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    enduits_sous_plafond_terrasse_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Enduits sous plafond"
    ).last()
    enduits_sous_plafond_terrasse_sable_quantity = round(
        float(enduits_sous_plafond_terrasse_sable.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    enduits_sous_plafond_terrasse_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Enduits sous plafond"
    ).last()
    enduits_sous_plafond_terrasse_gravier_quantity = round(
        float(enduits_sous_plafond_terrasse_gravier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    enduits_sous_plafond_terrasse_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Enduits sous plafond"
    ).last()
    enduits_sous_plafond_terrasse_eau_quantity = round(
        float(enduits_sous_plafond_terrasse_eau.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    enduits_sous_plafond_terrasse_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Enduits sous plafond"
    ).last()
    enduits_sous_plafond_terrasse_acier_quantity = round(
        float(enduits_sous_plafond_terrasse_acier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    # End Enduits sous plafond #

    # Enduits Exterieur #
    enduits_exterieur_terrasse = Quote_Project_Ouvrage.objects.filter(
        name="Enduits Exterieur", quote_project_step__name="Terrasse"
    ).last()
    enduits_exterieur_terrasse_quantity = round(
        float(enduits_exterieur_terrasse.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    enduits_exterieur_terrasse_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Enduits Exterieur"
    ).last()
    enduits_exterieur_terrasse_ciment_quantity = round(
        float(enduits_exterieur_terrasse_ciment.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    enduits_exterieur_terrasse_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Enduits Exterieur"
    ).last()
    enduits_exterieur_terrasse_sable_quantity = round(
        float(enduits_exterieur_terrasse_sable.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    enduits_exterieur_terrasse_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Enduits Exterieur"
    ).last()
    enduits_exterieur_terrasse_gravier_quantity = round(
        float(enduits_exterieur_terrasse_gravier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    enduits_exterieur_terrasse_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Enduits Exterieur"
    ).last()
    enduits_exterieur_terrasse_eau_quantity = round(
        float(enduits_exterieur_terrasse_eau.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    enduits_exterieur_terrasse_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Enduits Exterieur"
    ).last()
    enduits_exterieur_terrasse_acier_quantity = round(
        float(enduits_exterieur_terrasse_acier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    # End Enduits Exterieur #

    # Poteaux #
    poteaux_terrasse = Quote_Project_Ouvrage.objects.filter(
        name="Poteaux", quote_project_step__name="Terrasse"
    ).last()
    poteaux_terrasse_quantity = round(
        float(poteaux_terrasse.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    poteaux_terrasse_ciment = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Ciment", quote_project_ouvrage__name="Poteaux"
    ).last()
    poteaux_terrasse_ciment_quantity = round(
        float(poteaux_terrasse_ciment.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    poteaux_terrasse_sable = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Sable", quote_project_ouvrage__name="Poteaux"
    ).last()
    poteaux_terrasse_sable_quantity = round(
        float(poteaux_terrasse_sable.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    poteaux_terrasse_gravier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Gravier", quote_project_ouvrage__name="Poteaux"
    ).last()
    poteaux_terrasse_gravier_quantity = round(
        float(poteaux_terrasse_gravier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    poteaux_terrasse_eau = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Eau", quote_project_ouvrage__name="Poteaux"
    ).last()
    poteaux_terrasse_eau_quantity = round(
        float(poteaux_terrasse_eau.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level

    poteaux_terrasse_acier = Quote_Project_Materiaux.objects.filter(
        materiaux__name="Acier", quote_project_ouvrage__name="Poteaux"
    ).last()
    poteaux_terrasse_acier_quantity = round(
        float(poteaux_terrasse_acier.quantity * quote_project.area) / 3.5, 4
    ) * quote_project.level
    # End Poteaux #

    # Total Terrasse #
    total_quantity_ciment_terrasse = round(
        maconnerie_terrasse_ciment_quantity + coulage_cage_escalier_terrasse_ciment_quantity +
        mortier_terrasse_ciment_quantity + enduits_interieur_terrasse_ciment_quantity +
        enduits_sous_plafond_terrasse_ciment_quantity + enduits_exterieur_terrasse_ciment_quantity +
        poteaux_terrasse_ciment_quantity, 4
    )
    total_quantity_ciment_terrasse_int = int(total_quantity_ciment_terrasse)
    if total_quantity_ciment_terrasse_int == 0:
        total_quantity_ciment_terrasse_int = round(total_quantity_ciment_terrasse, 1)

    total_quantity_sable_terrasse = round(
        maconnerie_terrasse_sable_quantity + coulage_cage_escalier_terrasse_sable_quantity +
        mortier_terrasse_sable_quantity + enduits_interieur_terrasse_sable_quantity +
        enduits_sous_plafond_terrasse_sable_quantity + enduits_exterieur_terrasse_sable_quantity +
        poteaux_terrasse_sable_quantity, 4
    )
    total_quantity_sable_terrasse_int = int(total_quantity_sable_terrasse)
    if total_quantity_sable_terrasse_int == 0:
        total_quantity_sable_terrasse_int = round(total_quantity_sable_terrasse, 1)

    total_quantity_gravier_terrasse = round(
        maconnerie_terrasse_gravier_quantity + coulage_cage_escalier_terrasse_gravier_quantity +
        mortier_terrasse_gravier_quantity + enduits_interieur_terrasse_gravier_quantity +
        enduits_sous_plafond_terrasse_gravier_quantity + enduits_exterieur_terrasse_gravier_quantity +
        poteaux_terrasse_gravier_quantity, 4
    )
    total_quantity_gravier_terrasse_int = int(total_quantity_gravier_terrasse)
    if total_quantity_gravier_terrasse_int == 0:
        total_quantity_gravier_terrasse_int = round(total_quantity_gravier_terrasse, 1)

    total_quantity_eau_terrasse = round(
        maconnerie_terrasse_eau_quantity + coulage_cage_escalier_terrasse_eau_quantity + mortier_terrasse_eau_quantity
        + enduits_interieur_terrasse_eau_quantity + enduits_sous_plafond_terrasse_eau_quantity +
        enduits_exterieur_terrasse_eau_quantity + poteaux_terrasse_eau_quantity, 4
    )

    total_quantity_acier_terrasse = round(
        maconnerie_terrasse_acier_quantity + coulage_cage_escalier_terrasse_acier_quantity +
        mortier_terrasse_acier_quantity + enduits_interieur_terrasse_acier_quantity +
        enduits_sous_plafond_terrasse_acier_quantity + enduits_exterieur_terrasse_acier_quantity +
        poteaux_terrasse_acier_quantity, 4
    )
    total_quantity_acier_terrasse_int = int(total_quantity_acier_terrasse)
    if total_quantity_acier_terrasse_int == 0:
        total_quantity_acier_terrasse_int = round(total_quantity_acier_terrasse, 1)
    # End total Terrasse #

    # ############ End List of the ouvrages for the Terrasse step #############

    # ############ Total quote #############
    total_quantity_ciment_house = round(
        total_quantity_ciment_int + total_quantity_ciment_elevation_int + total_quantity_ciment_terrasse_int
        , 1)

    total_quantity_sable_house = round(
        total_quantity_sable_int + total_quantity_sable_elevation_int + total_quantity_sable_terrasse_int
        , 1)

    total_quantity_gravier_house = round(
        total_quantity_gravier_int + total_quantity_gravier_elevation_int + total_quantity_gravier_terrasse_int
        , 1)

    total_quantity_acier_house = round(
        total_quantity_acier_int + total_quantity_acier_elevation_int + total_quantity_acier_terrasse_int
        , 1)
    # ############ End Total quote #############

    return render(request, 'construction/automatic quote/automatic_quote_result.html', {
        'quote_project': quote_project, 'countries': countries, 'mesure_units': mesure_units, 'materiaux': materiaux,
        'quote_project_steps': quote_project_steps, 'mur_soubassement': mur_soubassement,
        'quote_project_materiaux_fondation_mur_soubassement': quote_project_materiaux_fondation_mur_soubassement,
        'mur_soubassement_quantity': mur_soubassement_quantity, 'mur_soubassement_ciment_quantity':
            mur_soubassement_ciment_quantity, 'mur_soubassement_sable_quantity': mur_soubassement_sable_quantity,
        'mur_soubassement_gravier_quantity': mur_soubassement_gravier_quantity, 'mur_soubassement_eau_quantity':
            mur_soubassement_eau_quantity, 'mur_soubassement_acier_quantity': mur_soubassement_acier_quantity,
        'beton_proprete_ciment_quantity': beton_proprete_ciment_quantity,
        'quote_project_materiaux_fondation_beton_proprete': quote_project_materiaux_fondation_beton_proprete,
        'beton_proprete': beton_proprete, 'beton_proprete_quantity': beton_proprete_quantity,
        'beton_proprete_sable_quantity': beton_proprete_sable_quantity, 'beton_proprete_gravier_quantity':
            beton_proprete_gravier_quantity, 'beton_proprete_eau_quantity': beton_proprete_eau_quantity,
        'beton_proprete_acier_quantity': beton_proprete_acier_quantity, 'semelles': semelles, 'semelles_quantity':
            semelles_quantity, 'quote_project_materiaux_fondation_semelles': quote_project_materiaux_fondation_semelles,
        'semelles_ciment_quantity': semelles_ciment_quantity, 'semelles_sable_quantity': semelles_sable_quantity,
        'semelles_gravier_quantity': semelles_gravier_quantity, 'semelles_eau_quantity': semelles_eau_quantity,
        'semelles_acier_quantity': semelles_acier_quantity, 'amorces_poteaux': amorces_poteaux,
        'amorces_poteaux_quantity': amorces_poteaux_quantity, 'quote_project_materiaux_fondation_amorces_poteaux':
            quote_project_materiaux_fondation_amorces_poteaux, 'amorces_poteaux_ciment_quantity':
            amorces_poteaux_ciment_quantity, 'amorces_poteaux_sable_quantity': amorces_poteaux_sable_quantity,
        'amorces_poteaux_gravier_quantity': amorces_poteaux_gravier_quantity, 'amorces_poteaux_eau_quantity':
            amorces_poteaux_eau_quantity, 'amorces_poteaux_acier_quantity': amorces_poteaux_acier_quantity,
        'longrines': longrines, 'longrines_quantity': longrines_quantity, 'quote_project_materiaux_fondation_longrines':
            quote_project_materiaux_fondation_longrines, 'longrines_ciment_quantity': longrines_ciment_quantity,
        'longrines_sable_quantity': longrines_sable_quantity, 'longrines_gravier_quantity': longrines_gravier_quantity,
        'longrines_eau_quantity': longrines_eau_quantity, 'longrines_acier_quantity': longrines_acier_quantity,
        'remblais': remblais, 'remblais_quantity': remblais_quantity, 'quote_project_materiaux_fondation_remblais':
            quote_project_materiaux_fondation_remblais, 'remblais_ciment_quantity': remblais_ciment_quantity,
        'remblais_sable_quantity': remblais_sable_quantity, 'remblais_gravier_quantity': remblais_gravier_quantity,
        'remblais_eau_quantity': remblais_eau_quantity, 'remblais_acier_quantity': remblais_acier_quantity,
        'total_quantity_ciment': total_quantity_ciment, 'total_quantity_sable': total_quantity_sable,
        'total_quantity_gravier': total_quantity_gravier, 'total_quantity_eau': total_quantity_eau,
        'total_quantity_acier': total_quantity_acier, 'total_quantity_ciment_int': total_quantity_ciment_int,
        'total_quantity_sable_int': total_quantity_sable_int, 'total_quantity_gravier_int':
        total_quantity_gravier_int, 'total_quantity_acier_int': total_quantity_acier_int, 'maconnerie': maconnerie,
        'maconnerie_quantity': maconnerie_quantity, 'maconnerie_ciment_quantity': maconnerie_ciment_quantity,
        'maconnerie_sable_quantity': maconnerie_sable_quantity, 'maconnerie_gravier_quantity':
        maconnerie_gravier_quantity, 'maconnerie_eau_quantity': maconnerie_eau_quantity,
        'maconnerie_acier_quantity': maconnerie_acier_quantity, 'linteaux': linteaux, 'linteaux_quantity':
        linteaux_quantity, 'linteaux_ciment_quantity': linteaux_ciment_quantity, 'linteaux_sable_quantity':
        linteaux_sable_quantity, 'linteaux_gravier_quantity': linteaux_gravier_quantity, 'linteaux_eau_quantity':
        linteaux_eau_quantity, 'linteaux_acier_quantity': linteaux_acier_quantity,
        'poutre': poutre, 'poutre_quantity': poutre_quantity, 'poutre_ciment_quantity': poutre_ciment_quantity,
        'poutre_sable_quantity': poutre_sable_quantity, 'poutre_gravier_quantity': poutre_gravier_quantity,
        'poutre_eau_quantity': poutre_eau_quantity, 'poutre_acier_quantity': poutre_acier_quantity, 'coulage': coulage,
        'coulage_quantity': coulage_quantity, 'coulage_ciment_quantity': coulage_ciment_quantity,
        'coulage_sable_quantity': coulage_sable_quantity, 'coulage_gravier_quantity': coulage_gravier_quantity,
        'coulage_eau_quantity': coulage_eau_quantity, 'coulage_acier_quantity': coulage_acier_quantity, 'mortier':
        mortier, 'mortier_quantity': mortier_quantity, 'mortier_ciment_quantity': mortier_ciment_quantity,
        'mortier_sable_quantity': mortier_sable_quantity, 'mortier_gravier_quantity': mortier_gravier_quantity,
        'mortier_eau_quantity': mortier_eau_quantity, 'mortier_acier_quantity': mortier_acier_quantity,
        'enduits_interieur': enduits_interieur, 'enduits_interieur_quantity': enduits_interieur_quantity,
        'enduits_interieur_ciment_quantity': enduits_interieur_ciment_quantity, 'enduits_interieur_sable_quantity':
        enduits_interieur_sable_quantity, 'enduits_interieur_gravier_quantity': enduits_interieur_gravier_quantity,
        'enduits_interieur_eau_quantity': enduits_interieur_eau_quantity, 'enduits_interieur_acier_quantity':
        enduits_interieur_acier_quantity, 'enduits_sous_plafond': enduits_sous_plafond,
        'enduits_sous_plafond_quantity': enduits_sous_plafond_quantity, 'enduits_sous_plafond_ciment_quantity':
        enduits_sous_plafond_ciment_quantity, 'enduits_sous_plafond_sable_quantity': enduits_sous_plafond_sable_quantity
        , 'enduits_sous_plafond_gravier_quantity': enduits_sous_plafond_gravier_quantity,
        'enduits_sous_plafond_eau_quantity': enduits_sous_plafond_eau_quantity, 'enduits_sous_plafond_acier_quantity':
        enduits_sous_plafond_acier_quantity, 'enduits_exterieur': enduits_exterieur, 'enduits_exterieur_quantity':
        enduits_exterieur_quantity, 'enduits_exterieur_ciment_quantity': enduits_exterieur_ciment_quantity,
        'enduits_exterieur_sable_quantity': enduits_exterieur_sable_quantity, 'enduits_exterieur_gravier_quantity':
        enduits_exterieur_gravier_quantity, 'enduits_exterieur_eau_quantity': enduits_exterieur_eau_quantity,
        'enduits_exterieur_acier_quantity': enduits_exterieur_acier_quantity, 'poteaux': poteaux, 'poteaux_quantity':
        poteaux_quantity, 'poteaux_ciment_quantity': poteaux_ciment_quantity, 'poteaux_sable_quantity':
        poteaux_sable_quantity, 'poteaux_gravier_quantity': poteaux_gravier_quantity,
        'poteaux_eau_quantity': poteaux_eau_quantity, 'poteaux_acier_quantity': poteaux_acier_quantity, 'escalier':
        escalier, 'escalier_quantity': escalier_quantity, 'escalier_ciment_quantity': escalier_ciment_quantity,
        'escalier_sable_quantity': escalier_sable_quantity, 'escalier_gravier_quantity': escalier_gravier_quantity,
        'escalier_eau_quantity': escalier_eau_quantity, 'escalier_acier_quantity': escalier_acier_quantity,
        'dallage_sol': dallage_sol, 'dallage_sol_quantity': dallage_sol_quantity,
        'dallage_sol_ciment_quantity': dallage_sol_ciment_quantity, 'dallage_sol_sable_quantity':
        dallage_sol_sable_quantity, 'dallage_sol_gravier_quantity': dallage_sol_gravier_quantity,
        'dallage_sol_eau_quantity': dallage_sol_eau_quantity, 'dallage_sol_acier_quantity':
        dallage_sol_acier_quantity, 'fosse_sceptique': fosse_sceptique, 'fosse_sceptique_quantity':
        fosse_sceptique_quantity, 'fosse_sceptique_ciment_quantity': fosse_sceptique_ciment_quantity,
        'fosse_sceptique_sable_quantity': fosse_sceptique_sable_quantity,
        'fosse_sceptique_gravier_quantity': fosse_sceptique_gravier_quantity, 'fosse_sceptique_eau_quantity':
        fosse_sceptique_eau_quantity, 'fosse_sceptique_acier_quantity': fosse_sceptique_acier_quantity,
        'total_quantity_ciment_elevation': total_quantity_ciment_elevation, 'total_quantity_sable_elevation':
        total_quantity_sable_elevation, 'total_quantity_gravier_elevation': total_quantity_gravier_elevation,
        'total_quantity_eau_elevation': total_quantity_eau_elevation, 'total_quantity_acier_elevation':
        total_quantity_acier_elevation, 'total_quantity_ciment_elevation_int': total_quantity_ciment_elevation_int,
        'total_quantity_sable_elevation_int': total_quantity_sable_elevation_int, 'total_quantity_gravier_elevation_int'
        : total_quantity_gravier_elevation_int, 'total_quantity_acier_elevation_int': total_quantity_acier_elevation_int
        , 'house_level': house_level, 'maconnerie_terrasse': maconnerie_terrasse, 'maconnerie_terrasse_quantity':
        maconnerie_terrasse_quantity, 'maconnerie_terrasse_acier_quantity': maconnerie_terrasse_acier_quantity,
        'maconnerie_terrasse_eau_quantity': maconnerie_terrasse_eau_quantity, 'maconnerie_terrasse_gravier_quantity':
        maconnerie_terrasse_gravier_quantity, 'maconnerie_terrasse_sable_quantity': maconnerie_terrasse_sable_quantity,
        'maconnerie_terrasse_ciment_quantity': maconnerie_terrasse_ciment_quantity,
        'coulage_cage_escalier_terrasse_ciment_quantity': coulage_cage_escalier_terrasse_ciment_quantity,
        'coulage_cage_escalier_terrasse_sable_quantity': coulage_cage_escalier_terrasse_sable_quantity,
        'coulage_cage_escalier_terrasse_gravier_quantity': coulage_cage_escalier_terrasse_gravier_quantity,
        'coulage_cage_escalier_terrasse_eau_quantity': coulage_cage_escalier_terrasse_eau_quantity,
        'coulage_cage_escalier_terrasse_acier_quantity': coulage_cage_escalier_terrasse_acier_quantity,
        'coulage_cage_escalier_terrasse_quantity': coulage_cage_escalier_terrasse_quantity,
        'coulage_cage_escalier_terrasse': coulage_cage_escalier_terrasse, 'mortier_terrasse_acier_quantity':
        mortier_terrasse_acier_quantity, 'mortier_terrasse_eau_quantity': mortier_terrasse_eau_quantity,
        'mortier_terrasse_gravier_quantity': mortier_terrasse_gravier_quantity, 'mortier_terrasse_sable_quantity':
        mortier_terrasse_sable_quantity, 'mortier_terrasse_ciment_quantity': mortier_terrasse_ciment_quantity,
        'mortier_terrasse': mortier_terrasse, 'mortier_terrasse_quantity': mortier_terrasse_quantity,
        'enduits_interieur_terrasse_acier_quantity': enduits_interieur_terrasse_acier_quantity,
        'enduits_interieur_terrasse_eau_quantity': enduits_interieur_terrasse_eau_quantity,
        'enduits_interieur_terrasse_gravier_quantity': enduits_interieur_terrasse_gravier_quantity,
        'enduits_interieur_terrasse_sable_quantity': enduits_interieur_terrasse_sable_quantity,
        'enduits_interieur_terrasse_ciment_quantity': enduits_interieur_terrasse_ciment_quantity,
        'enduits_interieur_terrasse': enduits_interieur_terrasse, 'enduits_interieur_terrasse_quantity':
        enduits_interieur_terrasse_quantity, 'enduits_sous_plafond_terrasse_acier_quantity':
        enduits_sous_plafond_terrasse_acier_quantity, 'enduits_sous_plafond_terrasse_eau_quantity':
        enduits_sous_plafond_terrasse_eau_quantity, 'enduits_sous_plafond_terrasse_gravier_quantity':
        enduits_sous_plafond_terrasse_gravier_quantity, 'enduits_sous_plafond_terrasse_sable_quantity':
        enduits_sous_plafond_terrasse_sable_quantity, 'enduits_sous_plafond_terrasse_ciment_quantity':
        enduits_sous_plafond_terrasse_ciment_quantity, 'enduits_sous_plafond_terrasse': enduits_sous_plafond_terrasse,
        'enduits_sous_plafond_terrasse_quantity': enduits_sous_plafond_terrasse_quantity,
        'enduits_exterieur_terrasse_acier_quantity': enduits_exterieur_terrasse_acier_quantity,
        'enduits_exterieur_terrasse_eau_quantity': enduits_exterieur_terrasse_eau_quantity,
        'enduits_exterieur_terrasse_gravier_quantity': enduits_exterieur_terrasse_gravier_quantity,
        'enduits_exterieur_terrasse_sable_quantity': enduits_exterieur_terrasse_sable_quantity,
        'enduits_exterieur_terrasse_ciment_quantity': enduits_exterieur_terrasse_ciment_quantity,
        'enduits_exterieur_terrasse': enduits_exterieur_terrasse, 'enduits_exterieur_terrasse_quantity':
        enduits_exterieur_terrasse_quantity, 'poteaux_terrasse_acier_quantity':
        poteaux_terrasse_acier_quantity, 'poteaux_terrasse_eau_quantity': poteaux_terrasse_eau_quantity,
        'poteaux_terrasse_gravier_quantity': poteaux_terrasse_gravier_quantity, 'poteaux_terrasse_sable_quantity':
        poteaux_terrasse_sable_quantity, 'poteaux_terrasse_ciment_quantity': poteaux_terrasse_ciment_quantity,
        'poteaux_terrasse': poteaux_terrasse, 'poteaux_terrasse_quantity': poteaux_terrasse_quantity,
        'total_quantity_ciment_terrasse': total_quantity_ciment_terrasse, 'total_quantity_sable_terrasse':
        total_quantity_sable_terrasse, 'total_quantity_gravier_terrasse': total_quantity_gravier_terrasse,
        'total_quantity_eau_terrasse': total_quantity_eau_terrasse, 'total_quantity_acier_terrasse':
        total_quantity_acier_terrasse, 'total_quantity_ciment_terrasse_int': total_quantity_ciment_terrasse_int,
        'total_quantity_sable_terrasse_int': total_quantity_sable_terrasse_int, 'total_quantity_gravier_terrasse_int':
        total_quantity_gravier_terrasse_int, 'total_quantity_acier_terrasse_int': total_quantity_acier_terrasse_int,
        'total_quantity_acier_house': total_quantity_acier_house, 'total_quantity_gravier_house':
        total_quantity_gravier_house, 'total_quantity_sable_house': total_quantity_sable_house,
        'total_quantity_ciment_house': total_quantity_ciment_house
    })
# ###################################### End Automatic quote ##################################################
# ###################################### End Automatic quote ##################################################
