#!flask/bin/python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

#adding items to database
class items(Base):
   __tablename__ = 'items'
   id = Column('item_id', Integer, primary_key = True)
   name = Column(String(100))
   category = Column(String(100))
   description = Column(String(200))
   nutrition = Column(String(200))
   ingredients = Column(String(200))
   price = Column(Integer)

   @property
   def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
	    'category' : self.category,
	    'description': self.description,
            'nutrition': self.nutrition,
	    'ingredients' : self.category,        
	    'price' : self.price
	}

engine = create_engine('sqlite:///items_temp_data.db')

Base.metadata.create_all(engine)
