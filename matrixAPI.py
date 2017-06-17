from flask import Flask, jsonify, request, Response, json, render_template

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
        return "The matrix " + name + " has been added to the list", 200
    else:
        matrices['name']['matrixdata'] = matrix['data']['matrixdata'] #if already exists, update it
        return "The matrix " + name + " already in the list, update the matrix data", 200

@app.route('/test/<string:name>')
def displayOne(name):
    if matrices[name] != None:
        return render_template("matrixTable.html", res = matrices[name]['matrixdata'],name=name), 200
    return "The " + name + " matrix does not store in the list."

@app.route('/test/<string:name>', methods=['DELETE'])
def deleteOne(name):
    if matrices[name] != None:
        matrices.pop(name, None)
        return "The matrix " + name + " has been deleted from the list."
    return "The matrix " + name + " is not in the list."

if __name__ == '__main__':
    app.run(debug=True,port=8080)