from flask_sqlalchemy import SQLAlchemy

#we will import this into models/items.py and models/stores.py 
#where we will instantiate classes that will handle the DB tables of the respective items
db = SQLAlchemy()



####### FROM THIS LINE DOWNWARD WE HAVE THE OLD DEPRECATED CODE#####

#stores={} Lists are now deprecated and we are using a relational database to store data, we use the flask-sqlachemy and sqlalchemy ORMs to do this
#items={} Lists are now deprecated and we are using a relational database to store data, we use the flask-sqlachemy and sqlalchemy ORMs to do this