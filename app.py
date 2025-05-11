#import the os library
import os

#import the secrets library to generate the secret key
#actually you don't use the library here run this liubrary
#in the terminal and obtain the rand bits as follows secrets.randbits(128)
#a safer way will be shown later 
import secrets

#import the flask and flasksmorest libraries
from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate

#import the database models created with SQLAlchemy
import models

#import the SQLalchemy package as defined in db.py
from db import db

#import blueprints we created and addded all the functions 
#of how APIs and their endpoints work
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBluePrint
from resources.user import blp as UserBluePrint

#import the JWT library for user authentication
#and security purposes
from flask_jwt_extended import JWTManager

#important that variable name and .py file are named app
#since "flask run" command will look in the venv for this parameters
#to activate the endpoints
#we use a function to create the app and return it
def create_app(db_url=None):
	
	#create the app instance
	app = Flask(__name__)

	#configure the app
	app.config["PROPAGATE_EXCEPTIONS"] = True
	app.config["API_TITLE"] = "Stores REST API"
	app.config["API_VERSION"] = "v1"
	app.config["OPENAPI_VERSION"] = "3.0.3"
	app.config["OPENAPI_URL_PREFIX"] = "/"
	app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
	app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
	app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	app.config["JWT_SECRET_KEY"] = "59812220736937944288788429558917247617"


	#initialise sqlachecmy extention of flask and connect it to sqlalchey to be able to load/handle the database models
	db.init_app(app)

	#before the app executes for the first time create the necessary tables
	#this is only needed when using SQLAlchemy
	#when we use flask migrate the below 2 lines are removed (here commented out)
	#with app.app_context():
	#	db.create_all()

	api = Api(app)

	migrate = Migrate(app, db) #flask migrate keeps track of all database model changes.


	jwt = JWTManager(app)

	@jwt.token_in_blocklist_loader
	def check_if_token_in_blocklist(jwt_header,jwt_payload):
		if models.BlockListModel.query.filter(
			models.BlockListModel.blocked_token == jwt_payload["jti"]).first():
				return True
		else:
			return False
	
	@jwt.revoked_token_loader
	def revoked_token_callback(jwt_header, jwt_payload):
		return(
			jsonify(
				{"description": "The token has been revoked", "error": "token revoked"}
			), 401
		)

		
		

	#the below functions are used to modify the return messages when authorisation fails across the various endpoints
	@jwt.expired_token_loader
	def expired_token_callback(jwt_header, jwt_payload):
		return (
              jsonify({"message": "The token has expired.", "error": "token_expired"}),
            	401,
        )

	@jwt.invalid_token_loader
	def invalid_token_callback(error):
		return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

	@jwt.unauthorized_loader
	def missing_token_callback(error):
		return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
    	)

	api.register_blueprint(ItemBlueprint)
	api.register_blueprint(StoreBlueprint)
	api.register_blueprint(TagBluePrint)
	api.register_blueprint(UserBluePrint)

	return app


