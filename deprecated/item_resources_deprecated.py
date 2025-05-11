##### THIS FILE IS DEPRECATED AFTER INTRODUCING MARSHMALLOW TO HANDLE VALIDATIONS
#### THE CODE TO BE FOLLOWED IS THE item.py file

import uuid #for generating unique ids
from flask import  request #request processes the json body into a dictionary
from flask_smorest import abort, Blueprint #will be used for posting messages during failure of calls and documentation
from flask.views import MethodView
from db import items,stores #refernces the dictionaries found in db.py (simulating database)

blp = Blueprint("Items", __name__, description="Operations on items.")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
	
	#this end point will get a single item
	def get(self, item_id):
		if item_id not in items:
			abort(404, message="Item not found.")
		else:
			return {"item" : items[item_id]}
		

	def put(self, item_id):
		item_data=request.get_json()
		if (
			"name" not in item_data 
			or "price" not in item_data
			):
				abort(400, message="Bad request. JSON payload should contain item 'name' and 'price'")
		try:
			item = items[item_id]
			item |= item_data
			return item
		except KeyError:
			abort(404, message="Item not found. Please check the 'item_id' is correct.")


	def delete(self, item_id):
		try:
			del items[item_id]
			return {"message": "Item deleted"}
		except KeyError:
			abort(404, message="Item not found.")


@blp.route("/item")
class ItemList(MethodView):

	def get(self):
		return {"items" : list(items.values())}

	def post(self):
		item_data = request.get_json()
		#proceeed with data check to ensure that everything needed is in payload
		if(
			"store_id" not in item_data 
			or "price" not in item_data 
			or "name" not in item_data
			):
				abort(
					400, 
					message="Bad request. 'Store_id', 'price' and 'name' are expected in the JSON payload."
					) #abort from flask_smorest has built in return and assists in documentation
		
		for item in items.values():
			if( #proceed with acheck to ensure no duplicate items for the same store
				item["name"] == item_data["name"]
				and item["store_id"] == item_data["store_id"]
			):
				abort(
					400,
					message = "Item already exists"
					)
			#proceed with a check that the store exists in the stores dictionary
			if item_data["store_id"] not in stores:
				abort(
					400, message = "Store not found."
				)
		else:
			item_id = uuid.uuid4().hex
			new_item = {**item_data, "id": item_id}
			items[item_id] = new_item
			return new_item, 201