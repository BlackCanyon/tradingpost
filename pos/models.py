from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.utils.timezone import now

# Create your models here.
class Customer(models.Model):
	camperID = models.IntegerField(primary_key=True)
	lastName = models.CharField(max_length=255)
	firstName = models.CharField(max_length=255)
	beginBalance = models.DecimalField(max_digits=6, decimal_places=2)
	currentBalance = models.DecimalField(max_digits=6, decimal_places=2)
	endBalance = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
	donateBalance = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
	returnedBalance = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2)
	downloadBalance = models.BooleanField()

	def __str__(self):
		return str(self.lastName + ", " + self.firstName)

class Category(models.Model):
	parentID = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
	categoryID = models.AutoField(primary_key=True)
	categoryDesc = models.CharField(max_length=255)

	def __str__(self):
		return self.categoryDesc

	class Meta:
		verbose_name_plural = "Categories"

class Item(models.Model):
	itemID = models.AutoField(primary_key=True)
	categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
	itemDesc = models.CharField(max_length=255)
	itemPrice = models.DecimalField(max_digits=5, decimal_places=2)

	def __str__(self):
		return self.itemDesc

class Style(models.Model):
	styleID = models.AutoField(primary_key=True)
	itemID = models.ForeignKey(Item, on_delete=models.CASCADE)
	styleDesc = models.CharField(max_length=255)

	def __str__(self):
		return self.styleDesc

class Color(models.Model):
	colorID = models.AutoField(primary_key=True)
	colorDesc = models.CharField(max_length=255)

	def __str__(self):
		return self.colorDesc

class Size(models.Model):
	sizeID = models.AutoField(primary_key=True)
	sizeDesc = models.CharField(max_length = 255)

	def __str__(self):
		return self.sizeDesc

class ItemColor(models.Model):
	itemID = models.ManyToManyField(Item)
	colorID = models.ManyToManyField(Color)

class ItemSize(models.Model):
	itemID = models.ManyToManyField(Item)
	sizeID = models.ManyToManyField(Size)

class Transaction(models.Model):
	transactionID = models.AutoField(primary_key=True)
	submitUser = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	camperID = models.ForeignKey(Customer, on_delete=models.CASCADE)
	transactionDate = models.DateTimeField(default=now)
	#transactionWeek = models.ForeignKey(Registration, on_delete=models.CASCADE)
	#itemCategory = models.ForeignKey(Category, on_delete=models.CASCADE) #Redundant, each item only has one category
	itemID = models.ForeignKey(Item, on_delete=models.CASCADE)
	#itemStyle = models.ForeignKey(Style, on_delete=models.CASCADE)
	itemColor = models.ForeignKey(Color, blank=True, null=True, on_delete=models.CASCADE)
	itemSize = models.ForeignKey(ItemSize, blank=True, null=True, on_delete=models.CASCADE)
	transactionNotes = models.CharField(blank=True, null=True, max_length=255)

	def calc_current_balance(ID):
		t = Transaction.objects.filter(camperID=ID).select_related('itemID')
		balance = list(Customer.objects.filter(pk=ID).values('beginBalance'))
		balance = balance[0]['beginBalance']
		deposit_sum = 0
		if Deposit.objects.filter(camperID=ID):
			deposit_sum = Deposit.objects.filter(camperID=ID)
			deposit_sum = deposit_sum.aggregate(Sum('depositAmount'))
			deposit_sum = deposit_sum['depositAmount__sum']

		if t:
			trans_sum = t.aggregate(Sum('itemID__itemPrice'))
			trans_sum = trans_sum['itemID__itemPrice__sum']

			curr_balance = balance - trans_sum + deposit_sum
			Customer.objects.filter(pk=ID).update(currentBalance = curr_balance)

			return

		else:
			curr_balance = balance + deposit_sum
			Customer.objects.filter(pk=ID).update(currentBalance = curr_balance)
			return

class Deposit(models.Model):
	depositID = models.AutoField(primary_key=True)
	camperID = models.ForeignKey(Customer, on_delete=models.CASCADE)
	depositDate = models.DateTimeField(default=now)
	depositAmount = models.DecimalField(max_digits=6, decimal_places=2)
	depositNotes = models.CharField(blank=True, null=True, max_length=255)