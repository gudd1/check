from django.conf import settings
from django.contrib import messages

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from testapp.forms import RegisterForm
from testapp.models import User

from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from django.contrib.auth import authenticate, login as auth_login

def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'pay.html')
    try:
        username = request.POST['username']
        password = request.POST['password']
        amount = int(request.POST['amount'])
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise ValueError
        auth_login(request=request, user=user)
    except:
        return HttpResponse(request,"Try again")
        '''return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})'''

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)



@csrf_exempt
def callback(request):
    print("came")
    return HttpResponse(request," create marchant ID")
    print("here")
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)



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


