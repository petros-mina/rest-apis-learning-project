from db import db

class StoreModel(db.Model):
	__tablename__ = "stores"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False, unique=True)

	#because we defined in item.py the PK/FK relationship 
	# SQLAlchemy can establish this connection with the items 
	# and can create an ItemModel and load the items of the specific store
	# which we can call within our code easily
	# the lazy parameter is that it loads only when called
	# and not with the API call, thus avoiding querying the db
	# the variable back_populates points to the "store" value found in the ItemModel class
	# the variable cascade ensures that we delete all items associated with the store upon deleting the store
	# this is to avoid Integrity errrors that arise when trying to retrieve aan item with a store 
	# that is now deleted since we have a constraint that says the store_id cannot be Null in the ItemModel class
	items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete") 
	tags = db.relationship("TagModel", back_populates="store", lazy="dynamic") 