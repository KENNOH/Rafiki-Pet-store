from __future__ import unicode_literals
from django.contrib import admin

from dashboard.models import Pet_type, Pet_services, Images, Transaction, C2BMessage, OnlineCheckoutResponse


class EventModelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_display_links = ["name"]
    list_filter = []
    list_per_page = 20
    list_editable = []

    class Meta:
        model = Pet_type


class EventModelAdmin1(admin.ModelAdmin):
    list_display = ["Type","contact_phone","contact_email","urlhash","description","created_at"]
    list_display_links = ["Type"]
    list_filter = []
    list_per_page = 20
    list_editable = []

    class Meta:
        model = Pet_services


class EventModelAdmin2(admin.ModelAdmin):
    list_display = ["urlhash","attachment"]
    list_display_links = ["urlhash"]
    list_filter = []
    list_per_page = 20
    list_editable = []

    class Meta:
        model = Images


admin.site.register(Pet_type, EventModelAdmin)
admin.site.register(Pet_services, EventModelAdmin1)
admin.site.register(Images, EventModelAdmin2)


    




