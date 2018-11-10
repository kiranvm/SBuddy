#!flask/bin/python
from flask import (
		Flask, 
		jsonify,
		request
)
#from flask_sqlalchemy import SQLAlchemy
#DB Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Items, Promotions

#db access part
engine = create_engine('sqlite:///items_temp_data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

items = [
    {
        'id': 1,
        'title': u'Krogers Wheat Bread',
        'description': u'Krogers Wheat Bread',
	'nutrition': u'testing nutrition',
	'ingredients': u'testing ingredients',
	'price': u'10'
    },
    {
        'id': 2,
        'title': u'Krogers Skimmed Milk',
        'description': u'Krogers Skimmed Milk',
	'nutrition': u'testing nutrition',
	'ingredients': u'testing ingredients',
	'price': u'10'
    }
]

success = [
    {
        'message': u'Success'
    }
]



@app.route('/sbuddy/api/v1.0/promotions',methods=['GET'])
def get_promotions():
    promotions = session.query(Promotions).all()
    return jsonify(Catalog=[i.serialize for i in promotions])

@app.route('/sbuddy/api/v1.0/items',methods=['GET'])
def get_items():
    #return jsonify({'items': items})
    list_items = session.query(Items).all()
    return jsonify(Catalog=[i.serialize for i in list_items])

@app.route('/sbuddy/api/v1.0/items/<int:item_id>', methods=['GET'])
def get_task(item_id):
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    return jsonify({'item': item[0]})

@app.route('/sbuddy/api/v1.0/add_items',methods=['POST'])
def add_item():
   if request.method == 'POST':
    item_name = request.form.get('name')
    item_category = request.form.get('category')
    item_description = request.form.get('description')
    item_nutrition = request.form.get('nutrition')
    item_ingredients = request.form.get('ingredients')
    item_price = request.form.get('price')

    newItem = Items(name=item_name, category=item_category,
             description=item_description,
	     nutrition = item_nutrition,
             ingredients = item_ingredients,
             price = item_price)
   
    session.add(newItem)
    session.commit()
    return jsonify({'response': success[0]})

if __name__ == '__main__':
	app.run(debug=True)
	
