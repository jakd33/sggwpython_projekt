from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import (Amenities, Hotel)
from django.db.models import Q


def home(request):
    amenities_objs = Amenities.objects.all()
    hotels_objs = Hotel.objects.all()

    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')
    print(amenities)
    if sort_by:
        if sort_by == 'ASC':
            hotels_objs = hotels_objs.order_by('hotel_price')
        elif sort_by == 'DSC':
            hotels_objs = hotels_objs.order_by('-hotel_price')

    if search:
        hotels_objs = hotels_objs.filter(
            Q(hotel_name__icontains = search) |
            Q(description__icontains = search) )


    if len(amenities):
        hotels_objs = hotels_objs.filter(amenities__amenity_name__in = amenities).distinct()

    context = {'amenities_objs' : amenities_objs , 'hotels_objs' : hotels_objs , 'sort_by' : sort_by 
    , 'search' : search , 'amenities' : amenities}
    return render(request , 'home.html' ,context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if not user_obj.exists():
            messages.warning(request, 'Nie znaleziono konta')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        user_obj = authenticate(username = username, password = password)
        
        if not user_obj:
            messages.warning(request, 'Nieprawidłowa nazwa użytkownika lub hasło')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        login(request, user_obj)
        return redirect('/')
    
    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        user_obj = User.objects.filter(username = username)

        if user_obj.exists():
            messages.warning(request, 'Nazwa użytkownika już istnieje')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if password1 != password2:
            messages.warning(request, 'Hasła różnią się, spróbuj jeszcze raz!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
        user = User.objects.create(username = username)
        user.set_password(password1)
        user.save()
        
        return redirect('/login')

    return render(request, 'register.html')

