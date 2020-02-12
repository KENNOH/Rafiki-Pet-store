from django.shortcuts import render, redirect
from dashboard.models import Pet_type, Pet_services, Images, Transaction, C2BMessage, OnlineCheckoutResponse
from dashboard.forms import ReviewForm
from django.contrib.auth.decorators import login_required
from .models import Review
from django.contrib import messages
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

@login_required
def make_review(request, urlhash):
	pet = Pet_services.objects.get(urlhash=urlhash)
	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			if not Review.objects.filter(customer=request.user, pet_instance=pet).exists():
				h = form.save(commit=False)
				h.customer = request.user
				h.pet_instance = pet
				h.owner = pet.user.username
				h.save()
				messages.info(request, "Processed successfully.")
				return redirect('pets_expand', urlhash=urlhash)
			else:
				messages.info(request, "You have already added a review,you cannot add another!")
				return redirect('pets_expand', urlhash=urlhash)
		else:
		    return render(request, 'home/add_review.html', {"form": form,'name':pet.user})
	else:
	    form = ReviewForm()
	    args = {'form': form, 'name': pet.user}
	    return render(request, 'home/add_review.html', args)

def sort(request,name):
	t = Pet_type.objects.all()
	tpe = t.get(name__icontains=name).name
	pets = Pet_services.objects.all().filter(Type=tpe)
	return render(request, 'home/pets_display.html', {'pets': pets, 't': t})
