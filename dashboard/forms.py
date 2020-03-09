from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from dashboard.models import Pet_type, Pet_services, Images, Transaction, C2BMessage, OnlineCheckoutResponse
from home.models import Review
from django.contrib.auth.forms import UserChangeForm


class PetForm(forms.ModelForm):
    Type = forms.ModelChoiceField(label="Select Pet type:", required=True, queryset=Pet_type.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control', 'name': 'Type'}))
    attachment = forms.FileField(label="Attachment:", required=True, widget=forms.ClearableFileInput(
        attrs={'multiple': True, 'name': 'attachment'}))
    # contact_email = forms.CharField(label='Contact Email:', max_length=200, required=True,widget=forms.TextInput(attrs={'class': 'form-control form-textbox'}))
    # contact_phone = forms.CharField(label='Contact Phone:', max_length=200, required=True,widget=forms.NumberInput(attrs={'class': 'form-control form-textbox'}))
    description = forms.CharField(label="Any Message?:", required=False, max_length=200, widget=forms.Textarea(
        attrs={'class': 'form-control form-textbox', 'name': 'description', 'rows': '4'}))
    location = forms.CharField(label='Location:', max_length=200, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control form-textbox'}))
    # quantity = forms.CharField(label='Quantity:', max_length=200, required=True,widget=forms.NumberInput(attrs={'class': 'form-control form-textbox'}))
    cost = forms.CharField(label='cost:', max_length=200, required=True,
                           widget=forms.NumberInput(attrs={'class': 'form-control form-textbox'}))
    thumbnail = forms.ImageField(label="Thumbnail Photo:", required=True, widget=forms.ClearableFileInput(
        attrs={'class': 'form-control', 'multiple': False, 'name': 'thumbnail'}))

    class Meta:
        model = Pet_services
        fields = ('Type', 'attachment', 'thumbnail',
                  'location', 'cost', 'description')

    def clean(self, *args, **kwargs):
        # contact_email = self.cleaned_data['contact_email']
        # if not contact_email:
        #     raise forms.ValidationError("Please a contact email.")
        return super(PetForm, self).clean(*args, **kwargs)

    def save(self, commit=True):
        Document = super(PetForm, self).save(commit=False)
        if commit:
            Document.save()
        return Document


class ServiceForm(forms.ModelForm):
    CHOICES = (
         ("Veterinary Services", "Veterinary Services"),
         ("Pet Sitters", "Pet Sitters"),
     )
    Type = forms.ChoiceField(label="Select Pet type:", required=True, choices=CHOICES,widget=forms.Select(attrs={'class': 'form-control', 'name': 'Type'}))
    attachment = forms.FileField(label="Images:", required=True, widget=forms.ClearableFileInput(attrs={'multiple': True, 'name': 'attachment'}))
    # contact_email = forms.CharField(label='Contact Email:', max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-textbox'}))
    # contact_phone = forms.CharField(label='Contact Phone:', max_length=200, required=True,widget=forms.NumberInput(attrs={'class': 'form-control form-textbox'}))
    description = forms.CharField(label="Any Message?:", required=False, max_length=200, widget=forms.Textarea(attrs={'class': 'form-control form-textbox', 'name': 'description', 'rows': '4'}))
    location = forms.CharField(label='Location:', max_length=200, required=True,widget=forms.TextInput(attrs={'class': 'form-control form-textbox'}))
    cost = forms.CharField(label='cost:', max_length=200, required=True,widget=forms.NumberInput(attrs={'class': 'form-control form-textbox'}))
    thumbnail = forms.ImageField(label="Thumbnail Photo:", required=True, widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': False, 'name': 'thumbnail'}))


    class Meta:
        model = Pet_services
        fields = ('Type', 'attachment', 'thumbnail','location', 'cost', 'description')

    def clean(self, *args, **kwargs):
        # contact_email = self.cleaned_data['contact_email']
        # if not contact_email:
        #     raise forms.ValidationError("Please a contact email.")
        return super(ServiceForm, self).clean(*args, **kwargs)

    def save(self, commit=True):
        Document = super(ServiceForm, self).save(commit=False)
        if commit:
            Document.save()
        return Document


class ReviewForm(forms.ModelForm):
    OPTIONS = (
        (1, 1),
        (2, 2),
        (3, 3),
      	(4, 4),
        (5, 5),
    )
    comment = forms.CharField(label="Make a comment:", required=False, max_length=200, widget=forms.Textarea(attrs={'class': 'form-control form-textbox', 'name': 'comment', 'rows': '3'}))
    rating = forms.ChoiceField(label="Select rating for this customer:", required=True, choices=OPTIONS,widget=forms.Select(attrs={'class': 'form-control form-textbox', 'name': 'rating'}))
    class Meta:
        model = Review
        fields = ('rating', 'comment')

    def clean(self, *args, **kwargs):
        return super(ReviewForm, self).clean(*args, **kwargs)

    def save(self, commit=True):
        Document = super(ReviewForm, self).save(commit=False)
        if commit:
            Document.save()
        return Document


class UpdateProfile(UserChangeForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
	    attrs={'class': 'form-control', 'placeholder': 'First name', 'name': 'first_name'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
	    attrs={'class': 'form-control', 'placeholder': 'Last name', 'name': 'last_name'}))
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(
	attrs={'class': 'form-control', 'readonly': 'readonly', 'placeholder': 'Enter your username', 'name': 'username'}))
    email = forms.CharField(max_length=75, required=True, widget=forms.TextInput(attrs={
	                        'class': 'form-control','readonly':True ,'id': 'exampleInputEmail1', 'placeholder': 'Enter your email', 'name': 'email'}))
    display_pic = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
		          'password', 'display_pic')
