from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from construction.forms import Construction_Project_Form, Construction_floor_Form, Architecture_Image_Form
from construction.models import Construction_Project, Construction_Type, Construction_floor, Architecture_Image, \
    Construction_Service
from real_estate.models import Land_Plan_Situation, Land_Paper_Type, Lands, Land_Project, Service_Type
from user.models import Construction_Projet_Tracker


def construction(request):
    if request.method == 'POST':
        if 'construction_project_submit' in request.POST:
            if request.user.is_authenticated:
                return redirect('construction_part1')
            else:
                messages.error(request, 'Veuillez vous connectez pour pouvoir commencer un projet de construction !')
                return redirect('login_user')

    return render(request, 'construction/construction.html')


def start_new_project(request):
    construction_project_services = Construction_Service.objects.all()
    if request.method == 'POST':
        construction_project_service_id = request.POST.get('construction_project_service_id')
        return redirect('construction_part1', construction_service_pk=construction_project_service_id)
    return render(request, 'construction/start_new_project.html', {'construction_project_services':
                                                                   construction_project_services})


def construction_part1(request, construction_service_pk):
    construction_project_services = Construction_Service.objects.all()
    construction_service = get_object_or_404(Construction_Service, pk=construction_service_pk)
    land_plan_situation = Land_Plan_Situation.objects.all()
    land_papier_types = Land_Paper_Type.objects.all()
    lands = Lands.objects.all()
    construction_types = Construction_Type.objects.all()
    land_projects = Land_Project.objects.filter(user=request.user)

    if request.method == 'GET':
        form_construction_project = Construction_Project_Form()
        return render(request, 'construction/construction_part1.html',
                      {'land_plan_situation': land_plan_situation,
                        'land_papier_types': land_papier_types, 'land_projects': land_projects, 'lands': lands,
                       'form_construction_project': form_construction_project, 'construction_types': construction_types,
                       'construction_service': construction_service, 'construction_project_services':
                       construction_project_services})
    else:
        try:
            form_construction_project = Construction_Project_Form(request.POST)
            if request.user.is_authenticated:
                if form_construction_project.is_valid():
                    #Saving the land infos for the consruction project#
                    form_construction_project = form_construction_project.save(commit=False)
                    form_construction_project.construction_type = get_object_or_404(Construction_Type,
                                                                 id=request.POST.get('construction_type_id'))
                    form_construction_project.user = request.user
                    form_construction_project.save()
                    # Creation of the contruction project tracker
                    new_tracker = Construction_Projet_Tracker(construction_project_id=form_construction_project.id)
                    new_tracker.save()

                    messages.success(request, 'Phase 1 terminée !')
                    return redirect('construction_part2', construction_project_pk=form_construction_project.id)

            else:
                messages.error(request, 'Veuillez vous connectez pour pouvoir commencer un projet de construction !')
                return redirect('login_user')
        except ValueError:
            return render(request, 'construction/construction_part1.html',
                      {'land_plan_situation': land_plan_situation, 'form_construction_project': form_construction_project,
                        'land_papier_types': land_papier_types, 'land_projects': land_projects, 'lands': lands,
                       'construction_types': construction_types, 'construction_service': construction_service,
                       'construction_project_services': construction_project_services,
                          'error': 'Mauvaises données saisies !'})


@login_required
def construction_part2(request, construction_project_pk):
    construction_project_services = Construction_Service.objects.all()
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    land_construction = Lands.objects.all()
    construction_types = Construction_Type.objects.all()
    land_papier_types = Land_Paper_Type.objects.all()
    land_plan_situation = Land_Plan_Situation.objects.all()
    construction_floors = Construction_floor.objects.filter(construction_project_id=construction_project_pk)
    number_floors = construction_project.number_floor + 1 #we added the floor 0 as a floor

    if 'complete_construction_project_info' in request.POST:
        if request.method == 'POST':
            messages.success(request, 'Votre demande a été envoyer avec succes, nous vous contacterons tres bientot !')
            return redirect('profile')

    if request.method == 'GET':
        form_construction_floor_project = Construction_floor_Form()
        return render(request, 'construction/construction_part2.html',
                      {'construction_project': construction_project, 'form_construction_floor_project':
                          form_construction_floor_project, 'construction_floors': construction_floors,
                           'land_construction': land_construction,
                           'construction_types': construction_types, 'number_floors': number_floors,
                           'land_papier_types': land_papier_types,
                           'land_plan_situation': land_plan_situation, 'construction_project_services':
                       construction_project_services})
    else:
        try:
            form_construction_floor_project = Construction_floor_Form(request.POST)
            if request.user.is_authenticated:
                #if construction_floors.floor
                if form_construction_floor_project.is_valid():
                    # Saving the land infos for the consruction project#
                    form_construction_floor_project = form_construction_floor_project.save(commit=False)
                    form_construction_floor_project.construction_project = get_object_or_404(Construction_Project,
                                                                                             id=construction_project.id)
                    form_construction_floor_project.save()
                    messages.success(request, 'Ce niveau a été enregistré avec succès !')
                    return redirect('construction_part2', construction_project_pk=construction_project_pk)

            else:
                messages.error(request, 'Veuillez vous connectez pour pouvoir commencer un projet de construction !')
                return redirect('login_user')
        except ValueError:
            return render(request, 'construction/construction_part2.html',
                          {'construction_project': construction_project, 'construction_floors': construction_floors,
                           'land_construction': land_construction,
                           'construction_types': construction_types, 'number_floors': number_floors,
                           'land_papier_types': land_papier_types, 'construction_project_services':
                               construction_project_services,
                           'land_plan_situation': land_plan_situation, 'error': 'Mauvaises données saisies !'})


@login_required
def clone_floor(request, construction_project_pk, construction_floor_pk):
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    land_construction = Lands.objects.all()
    construction_types = Construction_Type.objects.all()
    land_papier_types = Land_Paper_Type.objects.all()
    land_plan_situation = Land_Plan_Situation.objects.all()
    construction_floors = Construction_floor.objects.filter(construction_project_id=construction_project_pk)
    number_floors = construction_project.number_floor + 1  # we added the floor 0 as a floor
    construction_floor = get_object_or_404(Construction_floor, id=construction_floor_pk)

    if request.method == 'GET':
        form_construction_floor_project = Construction_floor_Form()
        return render(request, 'construction/clone_floor.html',
                      {'construction_project': construction_project, 'form_construction_floor_project':
                          form_construction_floor_project, 'construction_floor': construction_floor,
                           'land_construction': land_construction, 'construction_floors': construction_floors,
                        'number_floors': number_floors,
                           'construction_types': construction_types,
                           'land_papier_types': land_papier_types,
                           'land_plan_situation': land_plan_situation})
    else:
        try:
            form_construction_floor_project = Construction_floor_Form(request.POST)
            if request.user.is_authenticated:
                if form_construction_floor_project.is_valid():
                    # Saving the land infos for the consruction project#
                    form_construction_floor_project = form_construction_floor_project.save(commit=False)
                    form_construction_floor_project.construction_project = get_object_or_404(Construction_Project,
                                                                                             id=construction_project_pk)
                    form_construction_floor_project.save()
                    messages.success(request, 'Clonage effectuée avec succès !')
                    return redirect('construction_part2', construction_project_pk=construction_project_pk)

            else:
                messages.error(request, 'Veuillez vous connectez pour pouvoir commencer un projet de construction !')
                return redirect('login_user')
        except ValueError:
            return render(request, 'construction/clone_floor.html',
                          {'construction_project': construction_project, 'construction_floor': construction_floor,
                           'land_construction': land_construction, 'construction_floors': construction_floors,
                        'number_floors': number_floors,
                           'construction_types': construction_types,
                           'land_papier_types': land_papier_types,
                           'land_plan_situation': land_plan_situation, 'error': 'Mauvaises données saisies !'})


@login_required
def edit_floor(request, construction_project_pk, construction_floor_pk):
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    land_construction = Lands.objects.all()
    construction_types = Construction_Type.objects.all()
    land_papier_types = Land_Paper_Type.objects.all()
    land_plan_situation = Land_Plan_Situation.objects.all()
    construction_floor = get_object_or_404(Construction_floor, id=construction_floor_pk)

    if request.method == 'GET':
        form_construction_floor_project = Construction_floor_Form(instance=construction_floor)
        return render(request, 'construction/edit_floor.html',
                      {'construction_project': construction_project, 'form_construction_floor_project':
                          form_construction_floor_project, 'construction_floor': construction_floor,
                           'land_construction': land_construction,
                           'construction_types': construction_types,
                           'land_papier_types': land_papier_types,
                           'land_plan_situation': land_plan_situation})
    else:
        try:
            form_construction_floor_project = Construction_floor_Form(request.POST, instance=construction_floor)
            if request.user.is_authenticated:
                if form_construction_floor_project.is_valid():
                    #Saving the land infos for the consruction project#
                    form_construction_floor_project = form_construction_floor_project.save(commit=False)
                    form_construction_floor_project.construction_project = get_object_or_404(Construction_Project,
                                                                 id=construction_project_pk)
                    form_construction_floor_project.save()
                    messages.success(request, 'Modificatin effectuée avec succès !')
                    return redirect('construction_part2', construction_project_pk=construction_project_pk)

            else:
                messages.error(request, 'Veuillez vous connectez pour pouvoir commencer un projet de construction !')
                return redirect('login_user')
        except ValueError:
            return render(request, 'construction/edit_floor.html',
                          {'construction_project': construction_project, 'construction_floor': construction_floor,
                           'land_construction': land_construction,
                           'construction_types': construction_types,
                           'land_papier_types': land_papier_types,
                           'land_plan_situation': land_plan_situation, 'error': 'Mauvaises données saisies !'})


# @login_required
# def delete_floor(request, construction_project_pk, construction_floor_pk):
#     construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
#     construction_floor = get_object_or_404(Construction_floor, id=construction_floor_pk)
#
#     if request.method == 'GET':
#         return render(request, 'construction/delete_floor.html', {'construction_project':
#                                         construction_project, 'construction_floor': construction_floor})
#     if request.method == 'POST':
#         construction_floor.delete()
#         messages.success(request, 'Suppression effectuée !')
#         return redirect('construction_part2', construction_project_pk=construction_project_pk)


@login_required
def edit_construction_project(request, construction_project_pk):
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    construction_types = Construction_Type.objects.all()
    lands = Lands.objects.all()

    if request.method == 'GET':
        form = Construction_Project_Form(instance=construction_project)
        return render(request, 'construction/edit_construction_project.html', {'form': form, 'construction_project':
                                        construction_project, 'lands': lands,
                                                                   'construction_types': construction_types})
    else:
        try:
            form = Construction_Project_Form(request.POST, instance=construction_project)
            form = form.save(commit=False)
            form.construction_type = get_object_or_404(Construction_Type,
                                                         id=request.POST.get('construction_type_id'))
            form.save()
            messages.success(request, 'Modification éffectuée !')
            return redirect('construction_part2', construction_project_pk=construction_project_pk)
        except ValueError:
            return render(request, 'construction/edit_construction_project.html', {'form': form, 'construction_project':
                                                                    construction_project, 'lands': lands,
                                                                   'construction_types': construction_types,
                                                                       'error': 'Mauvaises données saisies !'})


@login_required
def delete_construction_project(request, construction_project_pk):
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    construction_types = Construction_Type.objects.all()
    lands = Lands.objects.all()

    if request.method == 'GET':
        return render(request, 'construction/delete_construction_project.html', {'construction_project':
                                        construction_project, 'lands': lands,
                                                                   'construction_types': construction_types})
    if request.method == 'POST':
        construction_project.delete()
        messages.success(request, 'Suppression effectuée !')
        return redirect('start_new_project')


@login_required
def construction_part3(request, construction_project_pk):
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    land_construction = Lands.objects.all()
    construction_types = Construction_Type.objects.all()
    land_papier_types = Land_Paper_Type.objects.all()
    land_plan_situation = Land_Plan_Situation.objects.all()
    construction_floors = Construction_floor.objects.filter(construction_project_id=construction_project_pk)
    construction_floors_count = Construction_floor.objects.filter(construction_project_id=construction_project_pk).count()
    number_floor_left = construction_project.number_floor - construction_floors_count
    images = Architecture_Image.objects.all()

    if 'complete_construction_project_info' in request.POST:
        if request.method == 'POST':
            messages.success(request, 'Votre demande a été envoyer avec succes, nous vous contacterons tres bientot !')
            return redirect('profile')

    if request.method == 'GET':
        architecture_image_form = Architecture_Image_Form()
        return render(request, 'construction/construction_part3.html',
                      {'construction_project': construction_project, 'architecture_image_form':
                          architecture_image_form, 'construction_floors': construction_floors,
                           'land_construction': land_construction, 'construction_floors_count': construction_floors_count,
                           'construction_types': construction_types, 'number_floor_left': number_floor_left,
                           'land_papier_types': land_papier_types, 'images': images,
                           'land_plan_situation': land_plan_situation})
    else:
        try:
            architecture_image_form = Architecture_Image_Form(request.POST, request.FILES)
            if request.user.is_authenticated:
                if architecture_image_form.is_valid():
                    # Saving the land infos for the consruction project#
                    architecture_image_form = architecture_image_form.save(commit=False)
                    architecture_image_form.construction_project = get_object_or_404(Construction_Project,
                                                                                     id=construction_project.id)
                    architecture_image_form.save()
                    messages.success(request, 'Image enregistrée avec succès !')
                    return redirect('construction_part3', construction_project_pk=construction_project_pk)

            else:
                messages.error(request, 'Veuillez vous connectez pour pouvoir commencer un projet de construction !')
                return redirect('login_user')
        except ValueError:
            return render(request, 'construction/construction_part3.html',
                          {'construction_project': construction_project, 'construction_floors': construction_floors,
                           'land_construction': land_construction, 'construction_floors_count': construction_floors_count,
                           'construction_types': construction_types, 'number_floor_left': number_floor_left,
                           'land_papier_types': land_papier_types, 'images': images,
                           'land_plan_situation': land_plan_situation, 'error': 'Mauvaises données saisies !'})