from django.contrib import admin
from .models import Customer, Transaction, Category, Item, Color, Size, ItemColor, ItemSize, Deposit
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
	list_display = ('camperID', 'lastName', 'firstName', 'currentBalance')

class TransactionAdmin(admin.ModelAdmin):
	list_display = ('transactionID', 'transactionDate', 'camperID', 'itemID')

	def save_model(self, request, obj, form, change):
		if not obj.submitUser:
			obj.submitUser = request.user
		obj.save()

class ItemAdmin(admin.ModelAdmin):
	list_display = ('itemID', 'itemDesc', 'itemPrice')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ItemColor)
admin.site.register(ItemSize)
admin.site.register(Deposit)