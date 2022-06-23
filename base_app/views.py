from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from base_app.forms import Notation_System_Form
from base_app.models import contact_message, Notation_System


def index(request):
    reviews = Notation_System.objects.all()
    if request.method == 'GET':
        notation_system_form = Notation_System_Form()
        return render(request, 'base_app/index.html', {'notation_system_form': notation_system_form, 'reviews': reviews})
    else:
        try:
            notation_system_form = Notation_System_Form(request.POST)
            if int(request.POST.get('stars')) < 6:
                if notation_system_form.is_valid():
                    notation_system_form = notation_system_form.save(commit=False)
                    notation_system_form.save()
                    messages.success(request, 'Merci, votre avis sera pris en compte !')
                    return redirect('index')
            else:
                messages.error(request, 'Le nombre doit être compris entre 1 et 5 ! ')
        except ValueError:
            return render(request, 'base_app/index.html', {'reviews': reviews, 'error': 'Mauvaises données saisies !'})


def contact_page(request):
    if request.method == "POST":
        try:
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            recipient_email = 'sheyp.sarl@gmail.com'
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            email_from = request.POST.get('email')
            recipient_list = [recipient_email, ]

            if phone_number.isnumeric():
                #Saving the message in the database
                message_sent = contact_message(full_name=full_name, email=email, subject=subject, phone_number=phone_number,
                                         message=message)
                message_sent.save()
                message1 = f'Nouveau message de la part de {full_name} \n Téléphone: {phone_number} \n Email: {email} \n' \
                           f'Contenu du message: {message}'
                send_mail(subject, message1, email_from, recipient_list)
                messages.success(request, f'Votre message à été envoyé avec succès, nous vous contacterons très bientôt !')
            else:
                messages.error(request, f'Le numéro de téléphone ne doit contenir que des chiffres, veuillez reéssayer !')
        except ValueError:
            return render(request, 'user/property_modification.html', {'error': 'Erreur, veuillez reéssayer !'})
    return render(request, 'base_app/contact_page.html')