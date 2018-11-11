from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Items, Promotions

engine = create_engine('sqlite:///items_temp_data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Some inital data for our database
item1 = Items(name="Peanut Butter", category="breakfast",
             description='Peanut Butter',
	     nutrition = 'Protein:10,fat:10,sugar:5',
             ingredients = 'peanuts,milk,sugar',
             price = 10,
             location = 'A10,5')

promotion1 = Promotions(name="Black Friday", category="All items",
             description='steep 10 % off',
             expirydate = '12/01/2018',
	     items = '10,11,12',
	     persona = 'healthy,fastfood')

session.add(item1)
session.add(promotion1)
session.commit()
