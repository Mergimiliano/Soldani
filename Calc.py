from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/calc/<operation>', methods=['GET'])
def calc(operation):
    n = request.args.get('n')
    m = request.args.get('m')

    if not n or not m or not operation:
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        n = float(n)
        m = float(m)
    except ValueError:
        return jsonify({'error': 'n and m need to be numbers'}), 400
    
    if operation == 'sum':
        result = n+m
        response = {'n':n, 'm':m, 'operation':'+', 'result':result}
    elif operation == 'difference':
        result = n-m
        response = {'n':n, 'm':m, 'operation':'-', 'result':result}
    elif operation == 'product':
        result = n*m
        response = {'n':n, 'm':m, 'operation':'*', 'result':result}
    elif operation == 'division':
        if m == 0:
            return jsonify({'error': 'Division by zero not allowed'}), 400
        result = n//m
        remainder = n%m
        response = {'n':n, 'm':m, 'operation':'*', 'result':result, 'remainder': remainder}
    else:
        return jsonify({'error': 'Operation not allowed'}), 400

    return jsonify(response)
    

if __name__ == '__main__':
    app.run(port=50003)