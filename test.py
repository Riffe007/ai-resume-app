from config.database import db

print("Collections in the database:", db.list_collection_names())
