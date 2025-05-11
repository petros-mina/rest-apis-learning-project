from db import db

class BlockListModel(db.Model):
	__tablename__ = "blocklist"

	id = db.Column(db.Integer,primary_key=True)
	blocked_token = db.Column(db.String(),nullable=False)