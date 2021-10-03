from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from testapp.forms import RegisterForm
from testapp.models import User


def home(request):

    return render(request, "shopping.html")
# Create your views here.
def register(request):
    if request.method!='GET':
       return HttpResponse("<h2>Method not allowed</h2>")
    else:
        form = RegisterForm()
        return render(request,"register.html",{'form':form})

def doregister(request):
    if request.method != 'POST':
        return HttpResponse("<h2> Mathod not Allowed!</h2>")
    else:

        Email = request.POST['E-mail']
        try:
            validate_email(Email)
        except ValidationError:
            messages.error(request, 'enter valid email')
        if (User.objects.filter(Q(email=request.POST['E-mail']))):
            messages.error(request, 'ID already registered!')
        else:
            newuser = User.objects.create_user(username=request.POST['username'],
                                                              password=request.POST['password'],
                                                              email=Email,
                                                              )

            newuser.save()
            messages.success(request, 'Registered Successfully!')
            return redirect('login')

        return render(request, 'register.html')


def login(request):
    if request.method!='GET':
       return HttpResponse("<h2>Method not allowed</h2>")
    else:
        return render(request,"login.html")

def dologin(request):
    return HttpResponse("you are logged in")

def upcoming(request):
    return render(request,"upcoming.html")

def brand(request,bname):

    return render(request,"brand.html",{"brand":bname})


