from dashboard.models import Transaction
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template.context_processors import csrf
from django_tables2 import RequestConfig
from dashboard.models import Pet_type, Pet_services, Images, Transaction, C2BMessage, OnlineCheckoutResponse
from accounts.models import Profile
from .forms import UpdateProfile
from dashboard.forms import PetForm, ServiceForm
from .tables import PetsTable, TransactionTable
import string 
import random 
from django_tables2 import RequestConfig
from .access_token import lipa_na_mpesa
from django.views.decorators.csrf import csrf_exempt
import base64
import json
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
import logging
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from .render import Render
from django.template.loader import get_template
from xhtml2pdf import pisa
from .utils import render_to_pdf
from django.http import HttpResponse
logger = logging.getLogger(__name__)

# Create your views here.


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Pet Owner').exists())
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Pet Owner').exists())
def start(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            Type = form.cleaned_data['Type']
            email = request.user.email
            u = request.user
            u.refresh_from_db()
            phone = u.profile.phone
            description = form.cleaned_data['description']
            loc = form.cleaned_data['location']
            cost = form.cleaned_data['cost']
            t = form.cleaned_data['thumbnail']
            rand = id_generator()
            Pet_services.objects.create(Type=Type, thumbnail=t, contact_email=email, cost=cost, contact_phone=phone,genre="Pet", description=description, urlhash=rand, user=request.user, location=loc)
            for file in request.FILES.getlist("attachment"):
                Images.objects.create(urlhash=rand,attachment=file)
            messages.info(request, "Processed successfully.")
            return HttpResponseRedirect('/dashboard/pets/')
        else:
            return render(request, 'dashboard/start.html', {"form": form})
    else:
        form = PetForm()
        args = {'form':form}
        return render(request, 'dashboard/start.html',args)


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Pet Owner').exists())
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            Type = form.cleaned_data['Type']
            email = request.user.email
            u = request.user
            u.refresh_from_db()
            phone = u.profile.phone
            description = form.cleaned_data['description']
            loc = form.cleaned_data['location']
            cost = form.cleaned_data['cost']
            t = form.cleaned_data['thumbnail']
            rand = id_generator()
            Pet_services.objects.create(Type=Type, thumbnail=t, contact_email=email, cost=cost, contact_phone=phone,description=description, urlhash=rand, user=request.user,genre="Service", location=loc)
            for file in request.FILES.getlist("attachment"):
                Images.objects.create(urlhash=rand, attachment=file)
            messages.info(request, "Service added successfully.")
            return HttpResponseRedirect('/dashboard/pets/')
        else:
            return render(request, 'dashboard/service.html', {"form": form})
    else:
        form = ServiceForm()
        args = {'form': form}
        return render(request, 'dashboard/service.html', args)


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Pet Owner').exists())
def check(request):
    pets = PetsTable(Pet_services.objects.all().filter(user=request.user).order_by('-created_at'))
    RequestConfig(request, paginate={"per_page": 20}).configure(pets)
    return render(request, 'dashboard/pets.html', {'pets': pets})


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Pet Owner').exists())
def trans(request):
    trans = TransactionTable(Transaction.objects.all().filter(user_id=request.user).order_by('-last_updated'))
    RequestConfig(request, paginate={"per_page": 20}).configure(trans)
    return render(request, 'dashboard/trans.html', {'trans': trans})


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Pet Owner').exists())
def expand_pet(request,pk):
    pet = Pet_services.objects.all().get(id=pk)
    pet_image = Images.objects.all().filter(urlhash=pet.urlhash)
    return render(request, 'dashboard/pet_expand.html', {'pet': pet,'image':pet_image})


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Pet Owner').exists())
def process_payment(request,urlhash):
    b = Pet_services.objects.get(urlhash=urlhash)
    u = request.user
    u.refresh_from_db()
    phone = u.profile.phone
    amount = 1
    try:
        data = {"phone": phone, "amount": amount, 'id': b.id}
        lipa_na_mpesa(data)
        messages.info(
            request, "Payment Initiated.Check your phone and enter pin to confirm.")
        return HttpResponseRedirect('/dashboard/pets/')
    except:
        messages.info(
            request, "There was an issue processing the payment ,Please try again.")
        return HttpResponseRedirect('/dashboard/pets/')


@csrf_exempt
def process_lnm(request):
    con = json.loads(request.read().decode('utf-8'))
    con1 = con["Body"]
    data = con1["stkCallback"]
    update_data = dict()
    update_data['result_code'] = data['ResultCode']
    update_data['result_description'] = data['ResultDesc']
    update_data['checkout_request_id'] = data['CheckoutRequestID']
    update_data['merchant_request_id'] = data['MerchantRequestID']
    meta_data = data['CallbackMetadata']['Item']
    if len(meta_data) > 0:
        # handle the meta data
        for item in meta_data:
            if len(item.values()) > 1:
                key, value = item.values()
                if key == 'MpesaReceiptNumber':
                    update_data['mpesa_receipt_number'] = value
                if key == 'Amount':
                    update_data['amount'] = Decimal(value)
                    a = update_data['amount']
                if key == 'PhoneNumber':
                    update_data['phone'] = int(value)
                    p = update_data['phone']
                if key == 'TransactionDate':
                    date = str(value)
                    year, month, day, hour, min, sec = date[:4], date[4:-
                                                                      8], date[6:-6], date[8:-4], date[10:-2], date[12:]
                    update_data['transaction_date'] = '{}-{}-{} {}:{}:{}'.format(
                        year, month, day, hour, min, sec)
    v = Pet_services.objects.get(mpesa_receipt_code=data['CheckoutRequestID'])
    v.status = 1
    v.save()
    Transaction.objects.create(user_id=v.user, amount=update_data['amount'], phone=update_data['phone'], mpesa_receipt_number=update_data['mpesa_receipt_number'])
    message = {"ResultCode": 0, "ResultDesc": "The service was accepted successfully","ThirdPartyTransID": "rafiki"}
    return JsonResponse({'message': message})


@login_required(login_url='/accounts/login/')
def update_profile(request):
    p = Profile.objects.get(user_id=request.user)
    if request.method == "POST":
        form = UpdateProfile(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if bool(form.cleaned_data.get('display_pic', False)) == False:
                form.save()
                messages.info(request, 'Profile updated successfully.')
                return HttpResponseRedirect('/dashboard/profile/')
            else:
                m = form.cleaned_data['display_pic']
                obj = p
				# if bool(obj.display_pic) == True:
				# 	if not str(obj.display_pic.name) == 'accounts/empty-profile.jpg':
				# 		os.remove(obj.display_pic.path)
                obj.display_pic = m
                form.save()
                obj.save()
                messages.info(request, 'Profile updated successfully.')
                return HttpResponseRedirect('/dashboard/profile/')
        else:
            form = UpdateProfile(instance=request.user)
            args = {'form': form, 'p': p}
            messages.info(request, 'Sorry ,there are errors in your form, fix them to continue.')
            return render(request, 'dashboard/profile.html', args)
    else:
        form = UpdateProfile(instance=request.user)
        args = {'form': form, 'p': p}
        return render(request, 'dashboard/profile.html', args)


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Pet Owner').exists())
def generate_pdf(request):
    hidden = request.POST['hidden']
    if hidden == 'transactions':
        trans = Transaction.objects.filter(user_id=request.user)
        template = get_template('dashboard/transactions_pdf.html')
        context = {'transactions': trans}
        html = template.render(context)
        pdf = render_to_pdf('dashboard/transactions_pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Transactions.pdf"
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        else:
            return HttpResponse("Not found")


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Pet Owner').exists())
def edit_pets(request,urlhash):
    pet = Pet_services.objects.get(urlhash=urlhash)
    if pet.genre == 'Pet':
        if request.method == "POST":
            form = PetForm(request.POST, request.FILES,instance=pet)
            if form.is_valid():
                if bool(form.cleaned_data.get('attachment', False)) == False:
                    form.save()
                    messages.info(request, 'Updated successfully.')
                    return HttpResponseRedirect('/dashboard/pets/')
                else:
                    form.save()
                    messages.info(request, 'Updated successfully.')
                    return HttpResponseRedirect('/dashboard/pets/')
            else:
                form = PetForm(request.POST,instance=pet)
                args = {'form': form}
                messages.info(request, 'Sorry ,there are errors in your form, fix them to continue.')
                return render(request, 'dashboard/edit_pet.html', args)
        else:
            form = PetForm(instance=pet)
            args = {'form': form}
            return render(request, 'dashboard/edit_pet.html', args)
    else:
        if request.method == "POST":
            form = ServiceForm(request.POST, request.FILES, instance=pet)
            if form.is_valid():
                if bool(form.cleaned_data.get('attachment', False)) == False:
                    form.save()
                    messages.info(request, 'Updated successfully.')
                    return HttpResponseRedirect('/dashboard/pets/')
                else:
                    form.save()
                    messages.info(request, 'Updated successfully.')
                    return HttpResponseRedirect('/dashboard/pets/')
            else:
                form = ServiceForm(request.POST, instance=pet)
                args = {'form': form}
                messages.info(request, 'Sorry ,there are errors in your form, fix them to continue.')
                return render(request, 'dashboard/edit_pet.html', args)
        else:
            form = ServiceForm(instance=pet)
            args = {'form': form}
            return render(request, 'dashboard/edit_pet.html', args)
