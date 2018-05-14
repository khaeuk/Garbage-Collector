from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib.auth.models import User

import datetime
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response, get_object_or_404
from userprof.models import ExtendedUser, AdminUser
from django.shortcuts import render
from garbage.models import Garbage, Watch
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
# from django.utils.six.moves.urllib.parse import urlparse


# Create your views here.
def home(request):
    garbages = Garbage.objects.all()
    context = {
        'garbage' : garbages
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


@login_required
def watch(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login")
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    if request.method == 'POST':
        #print(request.POST['pid'])
        pid = int(request.POST['id'])
        print(pid)
        garbage = get_object_or_404(Garbage, id=pid)  # TODO, switch to ID
        w = Watch(ExtendedUser=e_user, Garbage=garbage, date_watch = datetime.date.today())
        w.save()
    return render(request,'userprof.html')


def edit_item(request):
    if not request.user.is_authenticated:
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
        pid = request.POST['send']
        print(pid)
        form = GarbageEdit(request.POST)
        print(form)
        if form.is_valid():
            instance = get_object_or_404(Garbage, id=pid)
            instance.cost = int(form.cleaned_data['cost'])
            instance.title = form.cleaned_data['title']
            instance.condition = int(form.cleaned_data['condition'])
            instance.description = form.cleaned_data['description']
            instance.zipcode = int(form.cleaned_data['zipcode'])
            # form.photos = form.cleaned_data['photos']
            instance.save(force_update=True)
            return render(request, "sell.html")
    elif request.method == 'GET':
        pid = request.GET['edit']
        instance = get_object_or_404(Garbage, id=pid)  # TODO, switch to ID
        #print(instance)
        form = GarbageEdit(instance=instance)
    return render(request, "new_item.html", {'form': form, 'pid': pid})


def new_item(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_user = request.user
    e_user = ExtendedUser.objects.get(user=current_user)
    try:
        a_user = get_object_or_404(AdminUser, extended_user=e_user)
    except:
        return redirect('/home')
    print(a_user.extended_user.user.email)
    if a_user.registered is not True:
        return redirect('/home')
    if request.method == 'POST':
        instance = Garbage(owner=a_user)
        form = GarbageAdd(request.POST)
        print(form)
        form.owner = a_user
        if form.is_valid():
            instance.cost = int(form.cleaned_data['cost'])
            instance.title = form.cleaned_data['title']
            instance.condition = int(form.cleaned_data['condition'])
            instance.description = form.cleaned_data['description']
            instance.zipcode =int(form.cleaned_data['zipcode'])
            print(form.cleaned_data['cost'])
            instance.save();
            message_type = True
            message = "Item created successfully."
            request.session['message'] = message
            request.session['message_type'] = message_type
            return redirect(profile)
    elif request.method == 'GET':
        form = GarbageAdd()
    return render(request, "new_item.html", {'pid':Garbage.id })



def contact(request):
    return render(request, 'contact.html')

def sendEmail(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = "Garbage Collector Questions"
        from_email = email
        to_email = [settings.DEFAULT_FROM_EMAIL]

        context = {
        'user': name,
        'email': email,
        'message':message
        }

        send_mail(subject, message, from_email, to_email,fail_silently = True)

    return render(request,'contact.html')

def ItemDetails(request):
    pid = request.GET.get('garbage')
    instance = get_object_or_404(Garbage, id=pid)  # TODO, switch to ID
    context = {
        'title': instance.title,
        'description': instance.description,
        'cost': instance.cost,
        'photos': instance.photos,
        'zipcode': instance.zipcode,
        'condition': instance.condition,
        'distance': instance.distance,
        'owner':instance.owner,
        'postdate': instance.postdate,
        'solddate': instance.soldDate,
        'watched': instance.watched,

    }
    return render(request, 'ItemDetails.html', context)
