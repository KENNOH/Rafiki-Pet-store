from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.template.context_processors import csrf
from django_tables2 import RequestConfig
from dashboard.models import Pet_type, Pet_services, Images, Transaction, C2BMessage, OnlineCheckoutResponse
from dashboard.forms import PetForm
from .tables import PetsTable, TransactionTable
import string 
import random 
from django_tables2 import RequestConfig

# Create your views here.

def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))


def start(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            Type = form.cleaned_data['Type']
            email = form.cleaned_data['contact_email']
            phone = form.cleaned_data['contact_phone']
            description = form.cleaned_data['description']
            q = form.cleaned_data['quantity']
            loc = form.cleaned_data['location']
            cost = form.cleaned_data['cost']
            rand = id_generator()
            Pet_services.objects.create(Type=Type,contact_email=email,cost=cost,contact_phone=phone,description=description,urlhash=rand,user=request.user,quantity=q,location=loc)
            for file in request.FILES.getlist("attachment"):
                Images.objects.create(urlhash=rand,attachment=file)
            messages.info(request, "Processed successfully.")
            return HttpResponseRedirect('/dashboard/')
        else:
            return render(request, 'dashboard/start.html', {"form": form})
    else:
        form = PetForm()
        args = {'form':form}
        return render(request, 'dashboard/start.html',args)
    
def check(request):
    pets = PetsTable(Pet_services.objects.all().filter(user=request.user).order_by('-created_at'))
    RequestConfig(request, paginate={"per_page": 20}).configure(pets)
    return render(request, 'dashboard/pets.html', {'pets': pets})

def trans(request):
    trans = TransactionTable(Transaction.objects.all().filter(user_id=request.user).order_by('-last_updated'))
    RequestConfig(request, paginate={"per_page": 20}).configure(trans)
    return render(request, 'dashboard/trans.html', {'trans': trans})


def expand_pet(request,pk):
    pet = Pet_services.objects.all().get(id=pk)
    pet_image = Images.objects.all().filter(urlhash=pet.urlhash)
    return render(request, 'dashboard/pet_expand.html', {'pet': pet,'image':pet_image})
