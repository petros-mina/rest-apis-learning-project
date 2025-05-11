from flask_smorest import Blueprint, abort
from flask.views import MethodView
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError



from db import db
from models import UserModel, BlockListModel
from schemas import UserSchema, BlockListSchema

blp = Blueprint("Users", __name__, description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
	@blp.arguments(UserSchema)
	def post(self,user_data):
		if UserModel.query.filter(UserModel.username == user_data["username"]).first(): #this row leverages ORM to query the table of users and obtain the first result. If results exist then the same username exists. If no results are obtained (null) the we proceed
			abort(409, message="A user with the same username alreadu exists")
		else:
			user = UserModel (
				username = user_data["username"],
				password = pbkdf2_sha256.hash(user_data["password"])
			)

			db.session.add(user)
			db.session.commit()
		return {"message" : "user has been created"}, 201
	
@blp.route("/user/<int:user_id>")
class User(MethodView):
	@blp.response(200,UserSchema)
	def get(self, user_id):
		user = UserModel.query.get_or_404(user_id)
		return user
	
	def delete(self, user_id):
		user = UserModel.query.get_or_404(user_id)
		db.session.delete(user)
		db.session.commit()
		return {"message" : "user has been deleted."}, 200
	
@blp.route("/login")
class UserLogin(MethodView):
	@blp.arguments(UserSchema)
	def post(self, user_data):
		user = UserModel.query.filter(
			UserModel.username == user_data["username"]).first() #use the ORM to search for the username

		if user and pbkdf2_sha256.verify(user_data["password"],user.password): #if the user exists and the hashed password matches the saved hashed passoword then create an access token and return it
			access_token = create_access_token(identity = str(user.id))

			return {"access_token" : access_token}
		
		else:
			abort(401, message = "Credentials were invalid.")

@blp.route("/logout")
#the method obtains the jtwi from the header
#then uses it to create a blocklistmodel item
#adds the item to the database
#the database will be utilised as a blacklist
#any token in the blacklist is considered revoked
#thus any call made to an API tha tis jwt protected
#and the token is in the blackist
#the api will not be called
#the check of the table is within app.py
#where we define the token_in_blocklist_loader fuction
#to query the table of blocklist tokens
#if it identifies teh token it returns a True boolean
#and the boolean is the one that does the work courtesy of the jwt_extended library
class UserLogout(MethodView):
	@jwt_required()
	@blp.arguments(BlockListSchema)
	def post(self):
		jti = BlockListModel(blocked_token = get_jwt()["jti"])

		try:
			db.session.add(jti)
			db.session.commit()
		except SQLAlchemyError as e:
			abort(500, message="Something went wrong during logout. Logout unseccessful")
		
		return {"message" : "logout was succesful"}, 201