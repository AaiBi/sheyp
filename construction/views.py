from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from construction.forms import Construction_floor_Form
from construction.models import Construction_Project, Construction_Type, Construction_floor


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
        return render(request, 'construction/construction_part1.html',{'construction_types': construction_types})
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
    number_construction_floor = Construction_floor.objects.filter(construction_project_id=construction_project_pk)\
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
            #construction_floor_form = Architecture_Image_Form(request.POST, request.FILES)
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