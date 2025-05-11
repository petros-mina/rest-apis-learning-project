from marshmallow import Schema, fields

#we are creating a class that will hold the fields
#and we define how these fields behave in input/output manner 
#when the API is called 
#these are processed by flask and enrich our documentation

#this class defines the field types, their behaviour and their mandatory-ness for the post item function
class ItemSchema(Schema):
	id = fields.Str(dump_only=True) #this line says that id is not needed as input but only returned as output
	store_id = fields.Str(required=True) #this line says that when calling the API this parameter is mandatory
	name = fields.Str(required=True)
	price = fields.Float(required=True)

#this class defines the field types, their behaviour and their mandatory-ness for the put item function
class ItemSchemaUpdate(Schema):
	name = fields.Str() #this line means that this field is expected/used but not mandatory
	price = fields.Float()


#this class defines the field types, their behaviour and their mandatory-ness for the post store function
class StoreSchema(Schema):
	name = fields.Str(required=True)
	id = fields.Str(dump_only=True)