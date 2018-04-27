from django.shortcuts import render
from django.shortcuts import redirect
#from garbage.models import Garbage
from django.contrib.auth.models import User
from userprof.models import ExtendedUser
#from message.models import Message, ResMessage
from django.shortcuts import get_object_or_404
#import datetime
#import stripe

# Create your views here.
def profile(request):
    #message = request.session.pop('message', None)
    #message_type = request.session.pop('message_type', None)
    if not request.user.is_authenticated:
        return redirect('/home')

    current_user = request.user
    #parkingspots = []
    #incoming_requests = []
    #admin_user = False
    #m_user = get_object_or_404(ExtendedUser, main_user=current_user)
    #try:
        #a_user = get_object_or_404(AdminUser, extended_user=m_user)
        #parkingspots = ParkingSpot.objects.filter(owner=a_user)
        #incoming_requests = ResMessage.objects.filter(message__receiver=current_user, has_responded=False).order_by('res_date')
    admin_user = True
    #except:
    #    pass
    #messages = Message.objects.filter(receiver=current_user, is_reservation=False).order_by('-date')
    #outgoing_requests = ResMessage.objects.filter(message__sender=current_user).order_by('res_date')
    #now = datetime.datetime.now()
    #history = ResMessage.objects.filter(message__sender=current_user, res_date__lte = now, is_approved=True).order_by('res_date')
    context = {
        "admin_user": admin_user,
        #"message" : message,
        #"message_type" : message_type,
        #"incoming_requests" : incoming_requests,
        #"outgoing_requests" : outgoing_requests,
        #"messages"  : messages,
        #"parkingspots" : parkingspots,
        #"history": history
    }
    return render(request, "userprof.html")