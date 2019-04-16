from django import forms
from .models import Category, Transaction, Item, Customer

class TransactionForm(forms.Form):
	#class Meta:
	#	model = Transaction
	#	fields = ['camperID', 'transactionDate', 'itemID', 'itemColor']
	Camper = forms.ModelChoiceField(queryset=Customer.objects.all().order_by('lastName'))

class PurchaseForm(forms.Form):
	category = forms.ModelChoiceField(queryset=Category.objects.filter(parentID__isnull=True).order_by('categoryDesc'))
	subcategory = forms.ModelChoiceField(queryset=Category.objects.filter(parentID__isnull=False).order_by('categoryDesc'))
	item = forms.ModelChoiceField(queryset=Item.objects.all().order_by('itemDesc'))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['subcategory'].queryset = Category.objects.none()
		self.fields['item'].queryset = Item.objects.none()

class DepositForm(forms.Form):
	deposit = forms.DecimalField(max_digits=6, decimal_places=2)
	notes = forms.CharField(max_length=255)