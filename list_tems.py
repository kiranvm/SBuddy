from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Items, Promotions

engine = create_engine('sqlite:///items_temp_data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
list_items = session.query(Items).all()
for i in list_items:
	print (i)
