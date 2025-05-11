from db import db


class ItemModel(db.Model):

	__tablename__ = "items" #this creates a table called items

	id = db.Column(db.Integer, primary_key=True) #creates a column in the table that uses postgres serialisable property to autoincrement the id. It also does not allow to be NULL as a field
	name = db.Column(db.String(80), nullable=False) #creates a columnn of string with 80 chars as max
	price = db.Column(db.Float(precision=2), unique=False, nullable=False)
	store_id = db.Column(db.Integer, db.ForeignKey("stores.id") , unique=False, nullable=False) #defining the association between the 2 tables via establishing in which table and which field "stores.id"
	description = db.Column(db.String()) 
	tags = db.relationship("TagModel",back_populates="items",secondary="items_tags") #uses the items_tags table to retrieve all tags associated with the item



	
	#because we defined in item.py the PK/FK relationship 
	# SQLAlchemy can establish this connection with the store 
	# and can create an StoreModel and load the store associated with the specific item
	# which we can call within our code easily
	# the variable back_populates points to the "items" variable found in the StoreModel class
	store = db.relationship("StoreModel", back_populates="items") #because we defined the relationship with a store table via the db.ForeignKey paramater now we can have a StoreModel object that will link the store of the specific id and load it within the items
	