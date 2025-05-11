from flask_smorest import abort, Blueprint #will be used for posting messages during failure of calls and documentation
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from db import db #import the SQLAlchemy class as defined in db.py
from models import TagModel, StoreModel, ItemModel  #imprt the Model class that defines the  tables we want
from schemas import TagSchema, TagAndItemsSchema
from flask_jwt_extended import jwt_required

blp = Blueprint("Tags", "tags",description="Operation on tagsss")

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
	#get tags
	@blp.response(200, TagSchema(many=True))
	def get(self, store_id):
		store = StoreModel.query.get_or_404(store_id)
		
		return store.tags.all() #we utilise the filtering mechanism of the ORM of StoreModel to return the tags instead of wrting our own routine to do so

	#create tags
	@jwt_required()
	@blp.arguments(TagSchema)
	@blp.response(201, TagSchema)
	def post(self, tag_data, store_id):
		tag = TagModel(**tag_data, store_id=store_id)

		try: 
			db.session.add(tag)
			db.session.commit()
		except SQLAlchemyError as e:
			abort(500, message=str(e)) #cast the error to string in order to return it
		
		return tag
	
#retrieve specific tag info
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
	@blp.response(200, TagSchema)
	def get(self, tag_id):
		tag = TagModel.query.get_or_404(tag_id)

		return tag
	
	@jwt_required()
	@blp.response(
		202,
		description="Deletes a tag if not item is associated with it",
		example={"message": "Tage deleted"})
	@blp.alt_response(404, description="tag not found")
	@blp.alt_response(400, description="The tag is associated with other items in other stores and cannot be deleted")
	def delete(self, tag_id):
		tag = TagModel.query.get_or_404(tag_id)

		#check if the tag is not associated with any items
		#if so delete
		if not tag.items:
			try:
				db.session.remove(tag)
				db.session.commit()
				return {"message": "tag deleted"}
			except SQLAlchemyError:
				abort(500, message="There was an error during deleting the tag")
		abort(
			400, message="Tag cannot be deleted. It is associated with other items."
		) 
	

#use the below methods to link/unlink items to tags
@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItems(MethodView):
	@jwt_required()
	@blp.response(201, TagSchema)
	def post(self, item_id, tag_id):
		#find the item and tag and ensure they exist
		#since the item and tag are cretaed from other methods
		#we do this by the query.get_or_404 method of each model
		item = ItemModel.query.get_or_404(item_id)
		tag = TagModel.query.get_or_404(tag_id)

		item.tags.append(tag) #we add the tag to the item as the relationship of the secondary table is already defined in the item Model. we do not modifyu the item_tag table directly

		try:
			db.session.add(item)
			db.session.commit()
		except SQLAlchemyError:
			abort(500, message="An error occured while inserting the tag")
		
		return tag

	@blp.response(200, TagAndItemsSchema)
	@jwt_required()
	def delete(self, item_id, tag_id):
		item = ItemModel.query.get_or_404(item_id)
		tag = ItemModel.query.get_or_404(tag_id)

		item.tags.remove(tag) #removes the linking between the specific item and tag

		try:
			db.session.add(item)
			db.session.commit()
		except SQLAlchemyError:
			abort(500, message='An error occurred whilst trying to remove the tag')
		
		return {"message": "Tag removed from item", "item": item, "tag": tag}