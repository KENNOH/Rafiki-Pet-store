from django.shortcuts import render
from dashboard.models import Pet_type, Pet_services, Images, Transaction, C2BMessage, OnlineCheckoutResponse

# Create your views here.
def site(request):
	return render(request, 'home/home.html')


def pets_display(request):
	pets = Pet_services.objects.all()
	t = Pet_type.objects.all()
	img = Images.objects.all()
	return render(request, 'home/pets_display.html',{'pets':pets,'t':t,'img':img})

def pets_expand(request,urlhash):
	pet = Pet_services.objects.get(urlhash=urlhash)
	image = Images.objects.filter(urlhash=pet.urlhash)
	return render(request, 'home/pets_expand.html', {'pet': pet,'image':image})

def sort(request,name):
	t = Pet_type.objects.all()
	tpe = t.get(name__icontains=name).name
	pets = Pet_services.objects.all().filter(Type=tpe)
	return render(request, 'home/pets_display.html', {'pets': pets, 't': t})
