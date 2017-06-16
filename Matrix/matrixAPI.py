from flask import Flask, jsonify, request, Response, json

app = Flask(__name__)

matrices = {}

@app.route('/', methods = ['GET'])
def returnALL():
    return jsonify({'matrices': matrices})

@app.route('/test')
def test():
    return Response("Nothing")

@app.route('/test/<string:name>',methods=['PUT','POST'])
def addOne(name):
    matrix = request.json

    if matrices.get('name') == None:
        matrices.update({matrix['name']:matrix['data']})
    else:
        matrices['name']['matrixdata'] = matrix['data']['matrixdata'] #if already exists, update it

    return json.dumps(matrix), 200

@app.route('/test/<string:name>')
def displayOne(name):
    res = ""
    if matrices[name] != None:
        for row in matrices[name]['matrixdata']:
            for column in row:
                res += str(column) + " "
            res += "\n"
        return res

    return "The " + name + " matrix does not store in the list."


if __name__ == '__main__':
    app.run(debug=True,port=8080)