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
from models import (
		Base, 
		Items, 
		Promotions, 
		Recipe, 
		Users, 
		Recipe_Items,
                Personas
		)
#import json

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

noRecords = [
     {
	'message': u'No records present'
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
    
    for item_id in recipe_items.split(','): 
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


@app.route('/sbuddy/api/v1.0/bot_recipe/<int:recipe_id>',methods=['GET'])
def get_bot_recipe(recipe_id):
    recipe_items = session.query(Recipe_Items).filter(Recipe_Items.recipe_id == recipe_id).all()
    print(type(recipe_items))

    if recipe_items == None:
        abort(404)
    results = {}
    ls = []
    for e in recipe_items:
      i =  session.query(Items).filter(Items.id==e.item_id).first()
      if i != None:
         #results["items"]=ls.append({i.name:i.location})
         results["items"]={i.name:i.location}
	 
    return jsonify(results)



@app.route('/sbuddy/api/v1.0/list_recipe/<int:recipe_id>',methods=['GET'])
def get_recipe(recipe_id):
    recipe_items = session.query(Recipe_Items).filter(Recipe_Items.recipe_id == recipe_id).all()
    print(type(recipe_items))

    if recipe_items == None:
        abort(404)
    results = {}
    for e in recipe_items:
      i =  session.query(Items).filter(Items.id==e.id).first()
      if i != None:
         results["items"]={i.name:i.location}

    return jsonify(results)
    #return jsonify(recipe_items[0].serialize) #to be checked later 

@app.route('/sbuddy/api/v1.0/recipeByName', methods=['POST'])
def get_recipeByName():
    recipe_name=request.form.get('name')
    #recipe = ""
    if recipe_name != None:
     recipe_name=recipe_name.lower()
     recipe = session.query(Recipe).filter(Recipe.name.contains(recipe_name)).first()
     
     recipe_items = session.query(Recipe_Items).filter(Recipe_Items.recipe_id==recipe.id).all()

     results = {"name":recipe.name,"description":recipe.description,"items":[]}
     #items = []
     for item in recipe_items:
       print (item.id)
       i =  session.query(Items).filter(Items.id==item.id).first()
       #print(i.count)
       if i != None:
         print (i.name)
         results["items"]=results["items"].append({"name":i.name,"location":i.location})
         #cnt=cnt+1
	
    else:
     return jsonify({'response': noRecords[0]})
    if recipe == None:
        abort(404)
    #print (len(items))
    #return jsonify(recipe.serialize)
    return jsonify(results) 
    #return json.dumps(results)

@app.route('/sbuddy/api/v1.0/delete_recipe', methods=['POST'])
def delete_recipe():
    if request.method == 'POST':
      recipe = session.query(Recipe).filter(Recipe.id == request.form.get('id')).first()
      if recipe == None:
        abort(404)
      session.delete(recipe)
      session.commit()
    return jsonify({'response': success[0]}) 

'''
######################
Dashboard API methods
######################
'''
@app.route('/sbuddy/api/v1.0/dashboard',methods=['GET'])
def get_dashboard():
    items_count = session.query(Items).count()
    promotions_count = session.query(Promotions).count()
    recipes_count = session.query(Recipe).count()
    users_count = session.query(Users).count()
    personas_count = session.query(Personas).count()    

    persona_list = session.query(Users.persona).distinct()

    results = {}

    for personas in persona_list:
      print (type(personas))
      #print (session.query(Users).filter_by(persona=personas).count())
      results["personas"] = {str(personas):session.query(Users).filter_by(persona=str(personas)).count()}

    results['item_count'] = items_count
    results['promotions_count'] = promotions_count
    results['recipes_count'] = recipes_count
    results['personas_count'] = personas_count
    
    return jsonify(results)
    #return jsonify(Catalog=[i.serialize for i in list_recipes])
    #return jsonify({'response': success[0]})

'''
######################
Personas API methods
######################
'''
@app.route('/sbuddy/api/v1.0/list_personas',methods=['GET'])
def get_personas():
    list_personas = session.query(Personas).all()
    return jsonify(Personas=[i.serialize for i in list_personas])
    return jsonify({'response': success[0]})

@app.route('/sbuddy/api/v1.0/add_persona',methods=['POST'])
def add_persona():
   if request.method == 'POST':
    persona_name = request.form.get('name')
    persona_description = request.form.get('description')
    persona_tags = request.form.get('tags')

    newPersona = Personas(name=persona_name,
             description=persona_description,
	     tags=persona_tags)
    session.add(newPersona)
    session.commit()
    return jsonify({'response': success[0]})

@app.route('/sbuddy/api/v1.0/delete_persona', methods=['POST'])
def delete_persona():
    if request.method == 'POST':
      persona = session.query(Personas).filter(Personas.id == request.form.get('id')).first()
      if persona == None:
        abort(404)
      session.delete(persona)
      session.commit()
    return jsonify({'response': success[0]}) 

'''
######################
USERS API methods
######################

def add_user():
   if request.method == 'POST':
    user_name = request.form.get('name')
    user_email = request.form.get('email')
    user_persona = request.form.get('persona')
    user_queries = request.form.get('queries')

    newPersona = Personas(name=persona_name,
             description=persona_description,
	     tags=persona_tags)
    session.add(newPersona)
    session.commit()
    return jsonify({'response': success[0]})
'''

if __name__ == '__main__':
	app.run(debug=True)
	
