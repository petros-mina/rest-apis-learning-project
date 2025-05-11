from marshmallow import Schema, fields

#we are creating a class that will hold the fields
#and we define how these fields behave in input/output manner 
#when the API is called 
#these are processed by flask and enrich our documentation

#this class defines the field types, their behaviour and their mandatory-ness for the post item function
#the PlainItemSchema does not have the nested object from stores (Which can be brought in courtesy of SQLAlchemy)
#thus we also do not have the store_id in it
class PlainItemSchema(Schema):
	id = fields.Int(dump_only=True) #this line says that id is not needed as input but only returned as output
	name = fields.Str(required=True)
	price = fields.Float(required=True)

#this class defines the field types, their behaviour and their mandatory-ness for the put item function
class ItemSchemaUpdate(Schema):
	name = fields.Str() #this line means that this field is expected/used but not mandatory
	price = fields.Float()
	store_id = fields.Int()


#this class defines the field types, their behaviour and their mandatory-ness for the post store function
class PlainStoreSchema(Schema):
	name = fields.Str(required=True)
	id = fields.Int(dump_only=True)

class PlainTagSchema(Schema):
	id = fields.Int(dump_only=True)
	name = fields.Str(required=True)

#this schema inherits from PlainItemSchema all the values
#it also has the store_id and the store nested object
#defining both plain and non-plain schemas avoids the infinite recursion
#that can be created between items nesting stores which also nest items and so on and so forth
class ItemSchema(PlainItemSchema):
	store_id = fields.Int(required=True) #this line says that when calling the API this parameter is mandatory
	store = fields.Nested(PlainStoreSchema(), dump_only=True)
	tags = fields.List(fields.Nested(PlainTagSchema), dump_only=True)




#the class inherits from PlainStoreSchema 
#and also carries the nested object of items associated with the store
class StoreSchema(PlainStoreSchema):
	items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
	tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
	store_id = fields.Int(load_only=True)
	store = fields.Nested(PlainStoreSchema(), dump_only=True)
	items = fields.List(fields.Nested(PlainItemSchema), dump_ony=True) #this line is because we backpopulate tags with a list of items

class TagAndItemsSchema(Schema):
	message = fields.Str()
	item = fields.Nested(ItemSchema)
	tag = fields.Nested(TagSchema)

class UserSchema(Schema):
	user_id = fields.Int(dump_only=True) #dump_only property means we do not require the user to provide this
	username = fields.Str(required=True)
	password = fields.Str(required=True, load_only=True) #load only property, means the value is not returned by the API

#creating a schema for the Block token table
class BlockListSchema(Schema):
	blocklist_id = fields.Int(dump_only=True)
	blocked_token = fields.Str(required=True, load_only=True) #load_only to not return the value by the API