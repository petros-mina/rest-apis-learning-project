import uuid #for generating unique ids
from flask import request #request processes the json body into a dictionary
from flask_smorest import abort, Blueprint #will be used for posting messages during failure of calls and documentation
from flask.views import MethodView
from schemas import StoreSchema
from flask_jwt_extended import jwt_required

from db import db

from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from models import StoreModel

blp = Blueprint("Stores", __name__, description="Operations on stores.")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
	
	@blp.response(200,StoreSchema)
	def get(self, store_id):
		#the query method below comes from flasksqlalchemy
		#and tries to retrieve the store object 
		#and if it fails it also utilises the abort method
		store = StoreModel.query.get_or_404(store_id)
		return store

	@jwt_required()
	def delete(self, store_id):
		#the below setup tries to retrieve a store
		#if the store is not available it will raise an error
		#if the store is obtained it will still raise an error
		#flagging the fact that thereis no deletion method implemented yet
		store = StoreModel.query.get_or_404(store_id)
		db.session.delete(store)
		db.session.commit()
		return {"message" : "Store deleted."}

@blp.route("/store")
class StoreList(MethodView):

	@blp.response(200,StoreSchema(many=True))
	def get(self):#this function defines what is run at the specific end point
		#the .all() method is a cursor that will iterate over all stores
		#the StoreSchema(many=True) parameter will convert it to a list
		return StoreModel.query.all() 
		
	@jwt_required()
	@blp.arguments(StoreSchema)
	@blp.response(201, StoreSchema)
	def post(self,store_data):
		
		store = StoreModel(**store_data)

		try:
			db.session.add(store)
			db.session.commit()
		except IntegrityError:
			abort(400, message="A store with that name already exists.")
		except SQLAlchemyError:
			abort(500, message="An error occurred during insertion of the data in the stores table.")

		return store

