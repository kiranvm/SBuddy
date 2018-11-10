#!flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

items = [
    {
        'id': 1,
        'title': u'Krogers Wheat Bread',
        'description': u'Krogers Wheat Bread',
	'nutrition': u'testing nutrition',
	'ingredients': u'testing ingredients'
    },
    {
        'id': 2,
        'title': u'Krogers Skimmed Milk',
        'description': u'Krogers Skimmed Milk',
	'nutrition': u'testing nutrition',
	'ingredients': u'testing ingredients'
    }
]

@app.route('/sbuddy/api/v1.0/items',methods=['GET'])
def get_items():
    return jsonify({'items': items})

@app.route('/sbuddy/api/v1.0/items/<int:item_id>', methods=['GET'])
def get_task(item_id):
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    return jsonify({'item': item[0]})

if __name__ == '__main__':
	app.run(debug=True)
