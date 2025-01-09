from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/calc/<op>', methods=['GET'])
def calc(op):
    n = int(request.args.get('n'))
    m = int(request.args.get('m'))

    if not n or not m or not op:
        return jsonify({
            "error bad request": 400
        })
    
    if op == 'sum':
        result = n+m
        response = {'n':n, 'm':m, 'op':'+', 'result':result}
    elif op == 'difference':
        result = n-m
        response = {'n':n, 'm':m, 'op':'-', 'result':result}
    elif op == 'product':
        result = n*m
        response = {'n':n, 'm':m, 'op':'*', 'result':result}
    elif op == 'division':
        result = n//m
        remainder = n%m
        response = {'n':n, 'm':m, 'op':'*', 'result':result, 'remainder': remainder}

    return jsonify(response)
    

if __name__ == '__main__':
    app.run(port=50000)