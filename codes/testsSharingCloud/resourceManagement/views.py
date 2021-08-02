from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import signForm, bookForm
from .models import Users, Resource, Booking
import datetime
from django.contrib import messages
from django.urls import reverse

def index(request):
    template = loader.get_template('resourceManagement/base_index.html')
    return HttpResponse(template.render(request=request))
    
    
def signIn(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = signForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            email = form.cleaned_data['email']
            password = form.cleaned_data['password'] 
            userExist = Users.objects.filter(email=email).filter(password=password).exists()           
            # redirect to a new URL:
            if userExist:
                request.session['email'] = email
                return HttpResponseRedirect('base_user')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = signForm()

    return render(request, 'resourceManagement/signForm.html', {'form': form})

def base_user(request):
    template = loader.get_template('resourceManagement/base_user.html')
    return HttpResponse(template.render(request=request))


def book(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = bookForm(request.POST)
        
        # vérifier si le formulaire a été bien rempli:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            startDate = str(form.cleaned_data['startDate'])
            endDate = str(form.cleaned_data['endDate'])
            print(startDate)
            splitedStartDate = startDate[:10].split('-')
            splitedEndDate = endDate[:10].split('-')
            date1 = datetime.date(int(splitedStartDate[0].lstrip('0')), int(splitedStartDate[1].lstrip('0')), int(splitedStartDate[2].lstrip('0')))
            date2 = datetime.date(int(splitedEndDate[0].lstrip('0')), int(splitedEndDate[1].lstrip('0')), int(splitedEndDate[2].lstrip('0')))
            
            resource = form.cleaned_data['resource']
            
            #Vérifier si la 2éme date n'est pas inférieur à la première:
            if date1 > date2:               
                messages.add_message(request, messages.INFO, 'Veuillez choisir correctement vos dates.')
                return HttpResponseRedirect('book')
                
            else:
                #Si tout vas bien on vérifie s'il ny'a une réservation à la même date:
                all_booking_entries = Booking.objects.all()
                #bookExist = all_booking_entries.filter(startDate__startswith=startDate[:10]).filter(resource__resourceType=resource)
                bookExist = all_booking_entries.filter(startDate=startDate[:10]).filter(resource__resourceType=resource)
                if bookExist:
                    messages.add_message(request, messages.INFO,'Une réservation à cette date existe déjà ...')
                    return HttpResponseRedirect('book')
                
                #Sinon on enregistre la reservation.
                #Récupération de l'objet resource.
                resourceObject = Resource.objects.get(resourceType = resource)
                #Récupération de l'utilisateur:
                userObject = Users.objects.get(email = request.session['email'])
                #Création et sauvegarde de l'objet Réservation
                b = Booking(titleB = form.cleaned_data['title'], startDate = startDate[:10], endDate = endDate[:10], user = userObject, resource = resourceObject)
                b.save()
                messages.add_message(request, messages.INFO, 'Votre réservation a été prise en compte')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = bookForm()

    return render(request, 'resourceManagement/base_user_book.html', {'form': form})
    
    

def book_lists(request):

    #currentDate = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00.000000")
    #currentDateEnd = datetime.datetime.now().strftime("%Y-%m-%d 23:00:00.000000")
    
    #all_booking_entries_eq_currentDate = all_booking_entries \
    #.filter(user__email = request.session['email']) \
    #.select_related('resource').select_related('user') \
    #.filter(startDate__lte=currentDateEnd) \
    #.filter(startDate__gte=currentDate)
    
    currentDate = datetime.datetime.now().strftime("%Y-%m-%d")
    
    all_booking_entries = Booking.objects.all()
    
    all_booking_entries_lt_currentDate = all_booking_entries \
    .filter(user__email = request.session['email']) \
    .select_related('resource').select_related('user') \
    .filter(endDate__lt=currentDate)
    
    all_booking_entries_eq_currentDate = all_booking_entries \
    .filter(user__email = request.session['email']) \
    .select_related('resource').select_related('user') \
    .filter(startDate=currentDate) \
    .filter(endDate__gte=currentDate) | \
    all_booking_entries \
    .filter(user__email = request.session['email']) \
    .select_related('resource').select_related('user') \
    .filter(startDate__lte=currentDate) \
    .filter(endDate__gte=currentDate)
    
    all_booking_entries_gt_currentDate = all_booking_entries \
    .filter(user__email = request.session['email']) \
    .select_related('resource').select_related('user') \
    .filter(startDate__gt=currentDate)
    
    return render(request, 'resourceManagement/base_user_book_lists.html', \
    {'bookings_lt_currentDate' : all_booking_entries_lt_currentDate, \
    'bookings_eq_currentDate' : all_booking_entries_eq_currentDate, \
    'bookings_gt_currentDate' : all_booking_entries_gt_currentDate})
    
    
def edit_book(request, id_booking):
    b = Booking.objects.get(pk=id_booking)
    bData = {
        'title' : b.titleB,
        'startDate' : str(b.startDate),
        'endDate' : str(b.endDate),
        'resource' : b.resource.resourceType
    }
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        form = bookForm(request.POST)
        
        # vérifier si le formulaire a été bien rempli:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            startDate = str(form.cleaned_data['startDate'])
            endDate = str(form.cleaned_data['endDate'])
            
            splitedStartDate = startDate[:10].split('-')
            splitedEndDate = endDate[:10].split('-')
            date1 = datetime.date(int(splitedStartDate[0].lstrip('0')), int(splitedStartDate[1].lstrip('0')), int(splitedStartDate[2].lstrip('0')))
            date2 = datetime.date(int(splitedEndDate[0].lstrip('0')), int(splitedEndDate[1].lstrip('0')), int(splitedEndDate[2].lstrip('0')))
            
            resource = form.cleaned_data['resource']
            
            #Vérifier si la 2éme date n'est pas inférieur à la première:
            if date1 > date2:               
                messages.add_message(request, messages.INFO, 'Veuillez choisir correctement vos dates.')
                return HttpResponseRedirect(request.get_full_path())
                #return redirect(request.get_full_path)
                
            else:
                #Si tout vas bien on vérifie s'il ny'a une réservation à la même date:
                all_booking_entries = Booking.objects.all()
                #bookExist = all_booking_entries.filter(startDate__startswith=startDate[:10]).filter(resource__resourceType=resource)
                bookExist = all_booking_entries.filter(startDate=startDate[:10]).filter(resource__resourceType=resource)
                if bookExist:
                    messages.add_message(request, messages.INFO, 'Une réservation à cette date existe déjà ...')
                    return HttpResponseRedirect(request.get_full_path())
                
                #Sinon on enregistre la reservation.
                #Récupération de l'objet resource.
                resourceObject = Resource.objects.get(resourceType = resource)
                #Récupération de l'utilisateur:
                userObject = Users.objects.get(email = request.session['email'])
                #Création et sauvegarde de l'objet Réservation
                
                
                b.titleB = form.cleaned_data['title']
                b.startDate = startDate[:10]
                b.endDate = endDate[:10]
                b.user = userObject
                b.resource = resourceObject
                b.save()
                
                messages.add_message(request, messages.INFO, 'Votre réservation a été modifié !!!')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = bookForm(initial=bData)

    return render(request, 'resourceManagement/base_user_book_edit.html', {'form': form})
    
def delete_book(request, id_booking):
    if request.method == 'POST':
        instance = Booking.objects.get(pk=id_booking)
        instance.delete()
        messages.add_message(request, messages.INFO, 'Une réservation a été supprimé !!!')
        return HttpResponseRedirect(reverse('lists'))
        
    return render(request, 'resourceManagement/base_user_book_delete.html')
    