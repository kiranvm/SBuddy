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
def get_item(item_id):
    item = session.query(Items).filter(Items.id == item_id).first()
    #item = [item for item in items if item['id'] == item_id]
    if item == None:
        abort(404)
    return jsonify(item.serialize) 
    #print (item)
    #for key, val in events.items():
    #  print('{0}:\t{1}'.format(key,val))
    #return item.toJSON()
    #return jsonify({'item': item})

@app.route('/sbuddy/api/v1.0/add_promotions',methods=['POST'])
def add_promotion():
   if request.method == 'POST':
    prom_name = request.form.get('name')
    prom_category = request.form.get('category')
    prom_description = request.form.get('description')
    prom_expirydate = request.form.get('expirydate')
    prom_items = request.form.get('items')
    prom_persona = request.form.get('persona')

    newPromotion = Promotions(name=prom_name, 
             description=prom_description,
	     category = prom_category,
             expirydate = prom_expirydate,
             items = prom_items,
	     persona = prom_persona)
   
    session.add(newPromotion)
    session.commit()
    return jsonify({'response': success[0]})

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
	
