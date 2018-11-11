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
from models import Base, Items, Promotions, Recipe, Users, Recipe_Items

#db access part
engine = create_engine('sqlite:///items_temp_data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

success = [
    {
        'message': u'Success'
    }
]

'''
######################
Promotions API methods
######################
'''

@app.route('/sbuddy/api/v1.0/promotions',methods=['GET'])
def get_promotions():
    promotions = session.query(Promotions).all()
    return jsonify(Catalog=[i.serialize for i in promotions])


@app.route('/sbuddy/api/v1.0/promotions/<int:promotion_id>', methods=['GET'])
def get_promotion(promotion_id):
    promotion = session.query(Promotions).filter(Promotions.id == promotion_id).first()
    if promotion == None:
        abort(404)
    return jsonify(promotion.serialize) 

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

@app.route('/sbuddy/api/v1.0/delete_promotion', methods=['POST'])
def delete_promotion():
    if request.method == 'POST':
      promotion = session.query(Promotions).filter(Promotions.id == request.form.get('id')).first()
      if promotion == None:
        abort(404)
      session.delete(promotion)
      session.commit()
    return jsonify({'response': success[0]}) 

'''
######################
Items API methods
######################
'''

@app.route('/sbuddy/api/v1.0/items',methods=['GET'])
def get_items():
    list_items = session.query(Items).all()
    return jsonify(Catalog=[i.serialize for i in list_items])

@app.route('/sbuddy/api/v1.0/itemByName', methods=['POST'])
def get_itemByName():
    item_name=request.form.get('name').lower()
    #item = session.query(Items).filter(Items.id == item_id).first()
    item = session.query(Items).filter(Items.name.contains(item_name)).first()
    #item = [item for item in items if item['id'] == item_id]
    if item == None:
        abort(404)
    return jsonify(item.serialize) 

@app.route('/sbuddy/api/v1.0/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = session.query(Items).filter(Items.id == item_id).first()
    #item = [item for item in items if item['id'] == item_id]
    if item == None:
        abort(404)
    return jsonify(item.serialize) 

@app.route('/sbuddy/api/v1.0/delete_item', methods=['POST'])
def delete_item():
    if request.method == 'POST':
      item = session.query(Items).filter(Items.id == request.form.get('id')).first()
      if item == None:
        abort(404)
      session.delete(item)
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
    item_location = request.form.get('location')

    newItem = Items(name=item_name, category=item_category,
             description=item_description,
	     nutrition = item_nutrition,
             ingredients = item_ingredients,
             price = item_price,
             location = item_location)
   
    session.add(newItem)
    session.commit()
    return jsonify({'response': success[0]})

'''
######################
Recipes API methods
######################
'''
@app.route('/sbuddy/api/v1.0/add_recipe',methods=['POST'])
def add_recipe():
   if request.method == 'POST':
    recipe_name = request.form.get('name')
    recipe_description = request.form.get('description')
    recipe_items = request.form.get('items')

    newRecipe = Recipe(name=recipe_name,
             description=recipe_description)
    session.add(newRecipe)
    session.commit()

    recipe = session.query(Recipe).filter_by(name=recipe_name).first()
    
    for item_id in recipe_items: 
        print (recipe.id)
        print (item_id)  
        newItems = Recipe_Items(recipe.id,item_id)
        session.add(newItems)
    session.commit()

    return jsonify({'response': success[0]})

@app.route('/sbuddy/api/v1.0/list_recipes',methods=['GET'])
def get_recipes():
    list_recipes = session.query(Recipe).all()
    return jsonify(Catalog=[i.serialize for i in list_recipes])
    return jsonify({'response': success[0]})

@app.route('/sbuddy/api/v1.0/list_recipe/<int:recipe_id>',methods=['GET'])
def get_recipe(recipe_id):
    recipe_items = session.query(Recipe_Items).filter(Recipe_Items.recipe_id == recipe_id).all()
    print(type(recipe_items))
    for e in recipe_items:
     print (e.recipe_id)
    if recipe_items == None:
        abort(404)
    #return jsonify(catalog=[i.serialize() for i in recipe_items])
    return jsonify(recipe_items[0].serialize) #to be checked later 

if __name__ == '__main__':
	app.run(debug=True)
	
