from flask import  request #request processes the json body into a dictionary
from flask_smorest import abort, Blueprint #will be used for posting messages during failure of calls and documentation
from flask.views import MethodView
from schemas import ItemSchema, ItemSchemaUpdate
from flask_jwt_extended import jwt_required #this library is added as a decorator to functions that we want to protect. To call this functions the user must provide in the header a jwt token

from sqlalchemy.exc import SQLAlchemyError

from db import db #import the SQLAlchemy class as defined in db.py

from models import ItemModel #imprt the ItemModel class that defines the items table and the columns in order to create objects handled by SQLAlchemy

blp = Blueprint("Items", __name__, description="Operations on items.")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
	
	#this end point will get a single item
	@blp.response(200, ItemSchema) #we use response decorator for validation on what the API returns
	def get(self, item_id):
		#the query method below comes from flasksqlalchemy
		#and tries to retrieve the item object 
		#and if it fails it also utilises the abort method
		item = ItemModel.query.get_or_404(item_id)
		return item
	
	
	@jwt_required()
	@blp.arguments(ItemSchemaUpdate) # the output of ItemSchemaUpdate (we call it item_data) needs to go as input paramters before the blp.route arguments
	@blp.response(200, ItemSchema)
	def put(self, item_data, item_id):

		#first block tries to update the specific item if it exists
		#if it doesn't exist it will create an item an add it to the DB
		#this is the standard way of implementing put requests
		#in order to satisfy the idemtpotency property of apis 
		# Idempotency is a crucial property of certain operations or API requests
		# that guarantees consistent outcomes, 
		# regardless of the number of times an operation is performed. 
		item = ItemModel.query.get(item_id)
		if item:
			item.price = item_data["price"]
			item.name = item_data["name"]
		else:
			item = ItemModel(id=item_id, **item_data)
			db.session.add(item)
			db.session.commit()

		return item

	@jwt_required()
	def delete(self, item_id):
		item = ItemModel.query.get_or_404(item_id)
		db.session.delete(item)
		db.session.commit()
		return {"message": "Item deleted."}


@blp.route("/item")
class ItemList(MethodView):

	@blp.response(200, ItemSchema(many=True))
	def get(self):
		#the .all() method is a cursor that will iterate over all stores
		#the ItemSchema(many=True) parameter will convert it to a list
		return ItemModel.query.all()

	@jwt_required()
	@blp.arguments(ItemSchema) #this line uses the marshmallow method to process the arguments of the JSON payload according to the defined schema rules it then returns this as output (we call it item_data) which we will feed the post function below.
	@blp.response(201, ItemSchema) #note that the response decorator goes below the arguments decorator
	def post(self, item_data):
		
		item = ItemModel(**item_data) #unpacks the item_data json into the item using the definitions of columns of ItemModel

		try:
			db.session.add(item) #creates a session and in the session it adds to memory? the item. 
			db.session.commit() #you can do multiple operations in the session before commiting (ie writing) to the database using the .commit() function
		except SQLAlchemyError:
			abort(500, "An error occurred during insertion of data into the database on table 'items'.")
		
		return item