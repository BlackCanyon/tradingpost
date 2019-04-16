populate category dropdown with all categories where parentID == NULL

After user selects category
if parentID != NULL:
	populate subcategory menu with children
elif parentID == NULL:
	populate item menu with items

	  <td><a href="{% url 'delete_transaction' transaction.transactionID %}">delete</a></td>