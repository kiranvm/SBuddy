#!flask/bin/python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

#adding items to database
class Items(Base):
   __tablename__ = 'items'
   id = Column('item_id', Integer, primary_key = True)
   name = Column(String(100))
   category = Column(String(100))
   description = Column(String(200))
   nutrition = Column(String(200))
   ingredients = Column(String(200))
   price = Column(Integer)
   location = Column(String(50))

   @property
   def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
	    'category' : self.category,
	    'description': self.description,
            'nutrition': self.nutrition,
	    'ingredients' : self.ingredients,        
	    'price' : self.price,
            'location' : self.location
	}

#promotions
class Promotions(Base):
   __tablename__ = 'promotions'
   id = Column('promotions_id', Integer, primary_key = True)
   name = Column(String(100))
   category = Column(String(100))
   description = Column(String(200))
   expirydate = Column(String(200))
   items = Column(String(200))
   persona = Column(String(250))

   @property
   def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
	    'category' : self.category,
	    'description': self.description,
            'expirydate': self.expirydate,
	    'items' : self.items,        
	    'persona' : self.persona
	}

#users
class Users(Base):
   __tablename__ = 'users'
   id = Column('user_id', Integer, primary_key = True)
   name = Column(String(100))
   email = Column(String(100))
   persona = Column(String(100))
   queries = Column(String(200))
   items = Column(String(200))

   @property
   def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
	    'email' : self.email,
	    'persona': self.persona,
            'queries': self.queries,
	    'items' : self.items
	}

#recipe
class Recipe(Base):
   __tablename__ = 'recipes'
   id = Column('recipe_id', Integer, primary_key = True)
   name = Column(String(100))
   description = Column(String(200))

   @property
   def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
	    'description' : self.description
	}

class Recipe_Items(Base):
   __tablename__ = 'recipe_items'
   id = Column('recipeItems_id', Integer, primary_key = True)
   recipe_id = Column(String(100))
   item_id = Column(String(100))

   @property
   def serialize(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
	    'item_id' : self.item_id
	}
   def __init__(self, recipe_id, item_id):
     self.recipe_id = recipe_id
     self.item_id = item_id

#Personas
class Personas(Base):
   __tablename__ = 'personas'
   id = Column('persona_id', Integer, primary_key = True)
   name = Column(String(100))
   description = Column(String(200))
   tags = Column(String(500))

   @property
   def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
	    'description' : self.description,
            'tags' : self.tags
	}


engine = create_engine('sqlite:///items_temp_data.db')

Base.metadata.create_all(engine)
