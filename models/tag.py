from db import db


class TagModel(db.Model):
	
	__tablename__="tags"

	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(80),nullable=False, unique=True)
	#item_id = db.Column(db.Integer, db.ForeignKey("items.id"), unique=False)
	store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False)
	
	store = db.relationship("StoreModel", back_populates="tags")
	items = db.relationship("ItemModel", back_populates="tags",secondary="items_tags") #uses the items_tags table to retrieve all items associated with the tag