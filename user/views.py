from datetime import date
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from base_app.models import Provider
from construction.models import Construction_Project, Construction_Type, Construction_floor
from user.forms import EditUserInfoForm, EditUserInfoForm1, EditUserPasswordForm
from user.models import Customer, Cart, Construction_Projet_Tracker, \
    Construction_Tracker_Step, Construction_Tracker_Sub_Step, Construction_Tracker_Realisation, \
    Construction_Tracker_Realisation_Image, Construction_Expense, Step_Payment, Construction_Delivery, Delivery_Payment, \
    Construction_Delivery_Image


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
    #construction_project_services = Construction_Service.objects.all()
    construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
    construction_types = Construction_Type.objects.all()
    construction_floors = Construction_floor.objects.all()
    #images = Architecture_Image.objects.all()
    tracker = get_object_or_404(Construction_Projet_Tracker, construction_project_id=construction_project_pk)

    return render(request, 'user/construction_projects/construction_project_detail.html',
                  {'construction_project': construction_project, 'construction_types': construction_types,
                   'construction_floors': construction_floors, 'tracker': tracker})


# @login_required
# def edit_construction_floor(request, construction_project_pk, construction_floor_pk):
#     construction_project = get_object_or_404(Construction_Project, pk=construction_project_pk, user=request.user)
#     #land_construction = Lands.objects.all()
#     construction_types = Construction_Type.objects.all()
#     land_papier_types = Land_Paper_Type.objects.all()
#     land_plan_situation = Land_Plan_Situation.objects.all()
#     construction_floor = get_object_or_404(Construction_floor, id=construction_floor_pk)
#
#     if request.method == 'GET':
#         form_construction_floor_project = Construction_floor_Form(instance=construction_floor)
#         return render(request, 'user/construction_projects/edit_construction_floor.html',
#                       {'construction_project': construction_project, 'form_construction_floor_project':
#                           form_construction_floor_project, 'construction_floor': construction_floor,
#                            'construction_types': construction_types,
#                            'land_papier_types': land_papier_types,
#                            'land_plan_situation': land_plan_situation})
#     else:
#         try:
#             form_construction_floor_project = Construction_floor_Form(request.POST, instance=construction_floor)
#             if form_construction_floor_project.is_valid():
#                 #Saving the land infos for the consruction project#
#                 form_construction_floor_project = form_construction_floor_project.save(commit=False)
#                 form_construction_floor_project.construction_project = get_object_or_404(Construction_Project,
#                                                              id=construction_project_pk)
#                 form_construction_floor_project.save()
#                 messages.success(request, 'Modificatin effectuée avec succès !')
#                 return redirect('construction_project_detail', construction_project_pk=construction_project_pk)
#
#         except ValueError:
#             return render(request, 'user/construction_projects/edit_construction_floor.html',
#                           {'construction_project': construction_project, 'construction_floor': construction_floor,
#                            'construction_types': construction_types,
#                            'land_papier_types': land_papier_types,
#                            'land_plan_situation': land_plan_situation, 'error': 'Mauvaises données saisies !'})


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