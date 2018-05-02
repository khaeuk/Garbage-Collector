

from django.contrib.auth.models import User

import datetime
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response, get_object_or_404
from userprof.models import ExtendedUser, AdminUser
from django.shortcuts import render
from garbage.models import Garbage
from userprof.views import profile
from garbage.form import GarbageAdd, GarbageEdit
# from django.contrib.gis.measure import D #
# from django.contrib.gis.geos import Point
# from django.contrib.gis.geoip import GeoIP

from django.forms.models import model_to_dict

# from geopy.geocoders import GoogleV3
# from message.models import Message, ResMessage
from django.contrib.auth.models import User

import os
import json

from django.contrib.auth.decorators import login_required
from django.utils.six.moves.urllib.parse import urlparse



# Create your views here.
def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')

<<<<<<< HEAD

@login_required
def watch(request):
    if not request.user.is_authenticated():
        return redirect("/accounts/login")
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)


def new_item(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    try:
        a_user = get_object_or_404(AdminUser, extended_user=e_user)
    except:
        return redirect('/home')
    if a_user.registered is not True:
        return redirect('/home')
    if request.method == 'POST':
        instance = Garbage(owner=a_user)
        form = GarbageAdd(request.POST, request.FILES, instance=instance)
        form.owner = a_user
        if form.is_valid():
            instance.save()
            instance.photos = form.cleaned_data['photos']
            instance.save()
            form.save()
            message_type = True
            message = "Item created successfully."
            request.session['message'] = message
            request.session['message_type'] = message_type
            return redirect(profile)
    elif request.method == 'GET':
        form = GarbageAdd()
    return render(request, "editspot.html", {'form': form})

def contact(request):
    return render(request, 'contact.html')

