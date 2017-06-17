from flask import Flask, jsonify, request, Response, json, render_template

app = Flask(__name__)

matrices = {}

@app.route('/', methods = ['GET'])
def returnALL():
    return jsonify({'matrices': matrices})

@app.route('/test/<string:name>',methods=['PUT','POST'])
def addOne(name):
    '''
    PUT and POST method to add or revise a matrix in the dict
    :param name: the name of the matrix (key value in the dict)
    :return: the string that inform the user the matrix has been added
    '''
    try:
        matrix = request.json
        if matrices.get('name') == None:
            matrices.update({matrix['name']:matrix['data']})
            return "The matrix " + name + " has been added to the list", 200
        else:
            matrices['name']['matrixdata'] = matrix['data']['matrixdata'] #if already exists, update it
            return "The matrix " + name + " already in the list, update the matrix data", 200
    except Exception:
        error = {}
        error.update({'datatype':'status'})
        error.update({'statusmessage':"The input matrix does not right, check your json format"})
        error.update({'errorcode':11})
        return jsonify(error)

@app.route('/test/<string:name>')
def displayOne(name):
    '''
    GET method to display the matrix in the dict
    :param name: the name of the matrix (key value in the dict)
    :return: the matrix in HTML table format
    '''
    try:
        if matrices[name] != None:
            return render_template("matrixTable.html", res = matrices[name]['matrixdata'],name=name), 200
    except Exception:
        error = {}
        error.update({'datatype':'status'})
        error.update({'statusmessage':"The matrix " + name + " does not store in the list."})
        error.update({'errorcode':10})
        return jsonify(error)

@app.route('/test/<string:name>', methods=['DELETE'])
def deleteOne(name):
    '''
    DELETE the matrix in the dict
    :param name: the name of the matrix (key value in the dict)
    :return: the string inform user that the matrix has been deleted
    '''
    try:
        if matrices[name] != None:
            matrices.pop(name, None)
            return "The matrix " + name + " has been deleted from the list."
    except Exception:
        error = {}
        error.update({'datatype':'status'})
        error.update({'statusmessage':"The matrix " + name + " is not in the list."})
        error.update({'errorcode':10})
        return jsonify(error)

@app.errorhandler(404)
def page_not_found(e):
    return "The page you found does not match, check your spell!!(404)"

@app.errorhandler(405)
def request_wrong(e):
    return "The request method does not match. Check the request.(405)"

@app.errorhandler(Exception)
def all_exception_handler(error):
    return "Server is down, please check your url and try again.", 500

if __name__ == '__main__':
    app.run(debug=True,port=8080)