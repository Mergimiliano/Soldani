
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

items = {}

@app.route('/inventory', methods=['POST'])
def add_item():
    new_item = request.json

    if not new_item:
        return jsonify({'error': 'Missing body'}), 400

    if 'code' not in new_item:
        return jsonify({'error': 'Missing code'}), 400

    code = new_item['code']
    if code in items:
        return jsonify({'error': 'Item already registered'}), 409

    description = new_item.get('description', 'nd')
    quantity = new_item.get('quantity', 0)
    if not isinstance(quantity, int) or quantity < 0:
        return jsonify({'error': 'Quantity must be a non-negative integer'}), 400

    items[code] = {
        'description': description,
        'quantity': quantity
    }

    path = f'/inventory/{code}'

    response = make_response(jsonify({
        'code': code,
        'description': description,
        'quantity': quantity
    }), 201)
    response.headers['Location'] = path

    return response

@app.route('/inventory/<code>',methods=['GET'])
def get_item(code):
    # if code unknown, return error
    if code not in items:
        return jsonify({'error':True})
    # build & send reply
    return jsonify({
        'code': code,
        'description': items[code]['description'],
        'quantity': items[code]['quantity']
    })

@app.route('/inventory/<code>',methods=['PUT'])
def update_item(code):
    body = request.json
    code = body['code']
    # if code unknown, return error
    if code not in items:
        return jsonify({'error':True})
    # update item in inventory
    description = 'nd'
    if 'description' in body: 
        description = body['description']
    quantity = body['quantity']
    items[code] = {
        'description': description,
        'quantity': quantity
    }
    # build & send reply
    return jsonify({
        'code': code,
        'description': description,
        'quantity': quantity
    })

@app.route('/inventory/<code>',methods=['DELETE'])
def delete_item(code):
    if code not in items:
        return jsonify({'error': 'Item not found'}), 404
    items.pop(code)
    return jsonify({}), 200

if __name__ == '__main__':
    app.run(port=50000)
