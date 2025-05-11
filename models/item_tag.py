from db import db

#this table defines a many-to-many relationship between items and tags
#the table is utilised also to backpopulate tags into the items table and vice versa
class ItemTags(db.Model):
	__tablename__="items_tags"

	id = db.Column(db.Integer,primary_key=True)
	tag_id = db.Column(db.Integer,db.ForeignKey("tags.id")) 
	item_id = db.Column(db.Integer,db.ForeignKey("items.id"))