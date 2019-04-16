from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.edit import DeleteView

from .forms import TransactionForm, PurchaseForm, DepositForm
from .models import Customer, Category, Item, Transaction, Deposit

def transactionDelete(request, transaction_id):
	object = get_object_or_404(Transaction, pk=transaction_id)
	object.delete()

	form = TransactionForm()
	return HttpResponseRedirect((request.META.get('HTTP_REFERER', '/'))) 

def depositDelete(request, deposit_id):
	object = get_object_or_404(Deposit, pk=deposit_id)
	object.delete()

	form = TransactionForm()
	return HttpResponseRedirect((request.META.get('HTTP_REFERER', '/'))) 

def load_subcat(request):
	category = request.GET.get('category')
	subcats = Category.objects.filter(parentID=category).order_by('categoryDesc')
	return render(request, 'pos/subcat_dropdown_list_options.html', {'subcats': subcats})

def load_items(request):
	category = request.GET.get('category')
	items = Item.objects.filter(categoryID=category).order_by('itemDesc')
	return render(request, 'pos/item_dropdown_list_options.html', {'items': items})
# Create your views here.

def get_transaction(request):
	# if this is a POST request we need to process the form data
	transact_form = TransactionForm()
	if request.method == 'POST':
		data = request.POST.copy()
		if "item" in data:
			transaction = Transaction()
			transaction.camperID = Customer.objects.get(pk=request.GET['Camper'])
			transaction.itemID = Item.objects.get(pk=data.get('item'))
			transaction.save()
		else:
			form = DepositForm(request.POST)
			if form.is_valid():
				deposit = Deposit()
				deposit.camperID = Customer.objects.get(pk=request.GET['Camper'])
				deposit.depositAmount = form.cleaned_data['deposit']
				deposit.depositNotes = form.cleaned_data['notes']
				deposit.save()
	try:
		camperID = request.GET['Camper']
		transactionList = Transaction.objects.filter(camperID=camperID).select_related('itemID').order_by('-transactionDate')
		depositList = Deposit.objects.filter(camperID=camperID).order_by('-depositDate')
		trans_sum = Transaction.calc_current_balance(camperID)
		camper = Customer.objects.get(pk=camperID)
		purchase_form = PurchaseForm()
		deposit_form = DepositForm()
		return render(request = request,
					  template_name = 'pos/transaction.html',
					  context = {'transactionList' : transactionList,
					  			 'depositList' : depositList,
								 'camper' : camper,
								 'form' : transact_form,
								 'purchase_form' : purchase_form,
								 'deposit_form' : deposit_form})

	except MultiValueDictKeyError:
		transact_form = TransactionForm()

		return render(request = request,
					  template_name = 'pos/transaction.html',
					  context = {'form' : transact_form})