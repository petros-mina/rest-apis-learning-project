######## THE FILE IS DEPRECATED AFTER INTRODUCING SQLALCHEMY TO HANDLE DATA STORAGE


import uuid #for generating unique ids
from flask import  request #request processes the json body into a dictionary
from flask_smorest import abort, Blueprint #will be used for posting messages during failure of calls and documentation
from flask.views import MethodView
from db import items,stores #refernces the dictionaries found in db.py (simulating database)
from schemas import ItemSchema, ItemSchemaUpdate

blp = Blueprint("Items", __name__, description="Operations on items.")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
	
	#this end point will get a single item
	@blp.response(200, ItemSchema) #we use response decorator for validation on what the API returns
	def get(self, item_id):
		try:
			return items[item_id]
		except KeyError:
			abort(404, message="Item not found.")
		
	@blp.arguments(ItemSchemaUpdate) # the output of ItemSchemaUpdate (we call it item_data) needs to go as input paramters before the blp.route arguments
	@blp.response(200, ItemSchema)
	def put(self, item_data, item_id):
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

	@blp.response(200, ItemSchema(many=True))
	def get(self):
		return items.values()

	@blp.arguments(ItemSchema) #this line uses the marshmallow method to process the arguments of the JSON payload according to the defined schema rules it then returns this as output (we call it item_data) which we will feed the post function below.
	@blp.response(201, ItemSchema) #note that the response decorator goes below the arguments decorator
	def post(self, item_data):
		
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