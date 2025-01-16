from flask import Flask, request, jsonify

app = Flask(__name__)

users = {}

@app.route('/users', methods=['POST'])
def create_user():
    user = request.json
    nickname = user.get('nickname')
    name = user.get('name')
    surname = user.get('surname')
    email = user.get('email')

    if not nickname or not name or not surname or not email:
        return jsonify({'error': 'Required field missing'}), 400

    if nickname in users:
        return jsonify({'error': 'Nickname is already registered'}), 409

    users[nickname] = {
        'nickname': nickname,
        'name': name,
        'surname': surname,
        'email': email,
        'score': 0,
    }
    return jsonify({'user': users[nickname]}), 201

@app.route('/users/<nickname>', methods=['PUT'])
def update_user(nickname):
    updated_email = request.args.get('email')
    updated_name = request.args.get('name')
    updated_surname = request.args.get('surname')

    if not any([updated_email, updated_name, updated_surname]):
        return jsonify({'error': 'At least one parameter is required'}), 400
    
    user = users.get(nickname)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if updated_email:
        user['email'] = updated_email
    if updated_name:
        user['name'] = updated_name
    if updated_surname:
        user['surname'] = updated_surname
    
    return jsonify({'user': user}), 200

@app.route('/users/<nickname>', methods=['GET'])
def get_user(nickname):

    user = users.get(nickname)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'user': user}), 200

@app.route('/users/<nickname>', methods=['DELETE'])
def delete_user(nickname):

    user = users.get(nickname)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    users.pop(nickname)

    return jsonify({}), 200

@app.route('/scores/<nickname>', methods=['PUT'])
def set_score(nickname):
    score = request.json.get('score')

    if not score:
        return jsonify({'error': 'Required field missing'}), 400
    if not isinstance(score, (int, float)):
        return jsonify({'error': 'Invalid score value, must be a number'}), 400

    user = users.get(nickname)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user['score'] = score

    return jsonify(user), 200

if __name__ == '__main__':
    app.run(port=50006)