from __future__ import absolute_import ,unicode_literals
import django_tables2 as tables
from django.utils.html import format_html
from django_tables2.utils import A
from django.urls import reverse
from dashboard.models import Pet_type, Pet_services, Images, Transaction, C2BMessage, OnlineCheckoutResponse

class PetsTable(tables.Table):
	#edit = tables.LinkColumn('accept',args=[A('pk')],verbose_name="Action",orderable=False,empty_values=())
	#editable =  CheckBoxColumnWithName(verbose_name="Select", accessor="pk")
	urlhash = tables.LinkColumn('expand_pet',args=[A('pk')],verbose_name="Reference Code",orderable=True,empty_values=())
	# def render_edit(self,record):
	# 	if Document.objects.values_list('status',flat=True).get(order_number=record.pk)==False:
	# 		return format_html('<a href='+reverse("accept", args=[record.pk])+'><button type="button" class="form-control btn-success">Accept</button></a>')
	# 	else:
	# 		return format_html('<a href="#"><p>Accepted</p></a>')


	class Meta:
		model = Pet_services
		fields = ('urlhash','Type','location','cost','contact_phone','contact_email','cost','status')


class TransactionTable(tables.Table):
    class Meta:
        model = Transaction
        fields = ('mpesa_receipt_number', 'amount',
                  'phone', 'user_id', 'last_updated','status')
