import uuid #for generating unique ids
from flask import Flask, request #request processes the json body into a dictionary
from flask_smorest import abort #will be used for posting messages during failure of calls and documentation?
from db import items,stores #refernces the dictionaries found in db.py (simulating database)


#important that variable name and .py file are named app
#since "flask run" command will look in the venv for this parameters
#to activate the endpoints
app = Flask(__name__)

#create a data storage item as the first job to be dobe
#this  list (stores) will act as a temp db
#until a db is introduced
#each store will be a dictionary
#as per below structure
#ΤHE ITEM HAS BEEN COMMENTED OUT AND REPLACED WITH 
#DIFFERENT IMPLEMENTATION IN db.py
# stores = [
# 	{
# 		"name": "My Store",
# 		"items": [
# 			{
# 				"name" :"Chair",
# 				"price": 15.99
# 			}
# 		]
# 	}
# ]

#define the first endpoint
#this will be the get store endpoint
#when visiting the endpoint (http://127.0.0.1:5000/store)
#we will run the below function
@app.get("/store") #this line defines the end point
def get_stores():#this function defines what is run at the specific end point
	return {"stores": list(stores.values())}

#this end point will provide all the details of 
#a single store
@app.get("/store/<string:store_id>")
def get_store(store_id):
	try: 
		return stores[store_id] #will return from the stores dictinary the specific id
	except KeyError:
		abort(404, message="Store not found.")


#this endpoint/function will add a new store to the store list
#remember that lists to not persist so every time the program is killed
#the new stores wont exist. we will need to use a db for perisstence (later in course)
@app.post("/store")
def create_store():
	store_data = request.get_json() #this uses the request function from Flask to convert the JSON strinc into a dictionary
	if "name" not in store_data: #do a data check to ensure that 'name' is provided in payload
		abort(400, message="Bad request. Store 'name' must be provided in JSON payload.")
	
	for store in stores.values(): #do a data check to ensure that there no store with the same name
		if store["name"] == store_data["name"]:
			abort(400, message="Bad request. Another store with same name already exists.")
	store_id = uuid.uuid4().hex #uses uuid package to generate a unique id for the store
	new_store = {**store_data, "id" : store_id} 
	stores[store_id]=new_store
	return new_store, 201 #return the store back to the API call and the execution code

#this end point will get a single store
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
	try:
		del stores[store_id]
		return {"message": "Store deleted"}
	except KeyError:
		abort(404, message="Store not found.")


#this end point will return all the items of all stores
@app.get("/item")
def get_all_items():
	return {"items" : list(items.values())}


#this end point will get a single item
@app.get("/item/<string:item_id>")
def get_item(item_id):
	if item_id not in items:
		abort(404, message="Item not found.")
	else:
		return {"item" : items[item_id]}

#this endpoint will add items to the items dictionary in db.py
#the json payload already contains the store id 
@app.post("/item")
def create_item():
	item_data = request.get_json()
	#proceeed with data check to ensure that everything needed is in payload
	if(
		"store_id" not in item_data 
		or "price" not in item_data 
		or "name" not in item_data
		):
			abort(
				400, 
		 		message="Bad request. 'Store_id', 'price' and 'name' are expected in the JSON payload."
				) #abort from flask_smorest has built in return and assists in documentation
	
	for item in items.values():
		if( #proceed with acheck to ensure no duplicate items for the same store
			item["name"] == item_data["name"]
			and item["store_id"] == item_data["store_id"]
		):
			abort(
				400,
				message = "Item already exists"
				)
		#proceed with a check that the store exists in the stores dictionary
		if item_data["store_id"] not in stores:
			abort(
				400, message = "Store not found."
			)
	else:
		item_id = uuid.uuid4().hex
		new_item = {**item_data, "id": item_id}
		items[item_id] = new_item
		return new_item, 201

#this end point will update an item
@app.put("/item/<string:item_id>")
def update_item(item_id):
	item_data=request.get_json()
	if (
		"name" not in item_data 
		or "price" not in item_data
		):
			abort(400, message="Bad request. JSON payload should contain item 'name' and 'price'")
	try:
		item = items[item_id]
		item |= item_data
		return item
	except KeyError:
		abort(404, message="Item not found. Please check the 'item_id' is correct.")




#this end point will get a single item
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
	try:
		del items[item_id]
		return {"message": "Item deleted"}
	except KeyError:
		abort(404, message="Item not found.")

	

    
