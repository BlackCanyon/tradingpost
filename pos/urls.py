from django.urls import path

from . import views

urlpatterns = [
	path('', views.get_transaction, name='get_transaction'),
	path('<int:transaction_id>/delete-transaction/', views.transactionDelete, name='delete_transaction'),
	path('<int:deposit_id>/delete-deposit/', views.depositDelete, name='delete_deposit'),
	path('ajax/load-subcat/', views.load_subcat, name='ajax_load_subcat'),
	path('ajax/load-items/', views.load_items, name='ajax_load_items'),
]