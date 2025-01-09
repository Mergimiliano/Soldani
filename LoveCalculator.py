from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/love', methods=['GET'])
def love():
    lover1 = request.args.get('lover1')
    lover2 = request.args.get('lover2')
    affinity = (hash(lover1) + hash(lover2))%101

    if not lover1 or not lover2:
        return jsonify({
            "error bad request": 400
        })

    response = {'lover1':lover1, 'lover2':lover2, 'affinity': affinity}
    return jsonify(response)
    

if __name__ == '__main__':
    app.run(port=50000)