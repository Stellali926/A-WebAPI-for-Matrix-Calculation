from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

matrices = {}

@app.route('/', methods = ['GET'])
def returnALL():
    return render_template("welcome.html", storedMatrix = matrices)

@app.route('/matrices/<string:name>',methods=['PUT','POST'])
def addOne(name):
    '''
    PUT and POST method to add or revise a matrix in the dict
    :param name: the name of the matrix (key value in the dict)
    :return: the string that inform the user the matrix has been added
    
    (The example json format of the matrix is:)
    {
	"datatype": "Matrix",
	"name": "A",
	"data":{
		"numrows":2,
		"numcols":2,
		"matrixdata":[[2,2],[2,2]]
		}
	}
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

@app.route('/matrices/<string:name>')
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

@app.route('/matrices/<string:name>', methods=['DELETE'])
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

@app.route('/calculations', methods=['POST'])
def do_calculations():
    '''
    POST call realize the matrix calculations including add, subtraction and multiplication
    :return: The matrix after the calculation in HTML table format
    
    (The example input json format: )
    {
	"datatype": "operation",
	"operationtype": "add",
	"operand1": "A",
	"operand2": "B",
	"resultant": "C"
    }
    '''
    calRequest = request.json
    operand1 = calRequest['operand1']
    operand2 = calRequest['operand2']
    #If the operation type is add or subtraction, use two loops to get the new matrix
    if calRequest['operationtype'] == 'add' or calRequest['operationtype'] == 'subtraction':
        # judge whether the matrices are eligible to do the add or subtraction
        if matrices[operand1]['numcols'] == matrices[operand2]['numcols'] and matrices[operand1]['numrows'] == matrices[operand2]['numrows']:
            row = 0
            resRow = []  #initialize the new matrix
            while(row < matrices[operand1]['numrows']):
                resCol = []
                col = 0
                while(col < matrices[operand1]['numcols']):
                    if calRequest['operationtype'] == 'add':
                        resCol.append(matrices[operand1]['matrixdata'][row][col] + matrices[operand2]['matrixdata'][row][col])
                    else:
                        resCol.append(matrices[operand1]['matrixdata'][row][col] - matrices[operand2]['matrixdata'][row][col])
                    col += 1
                resRow.append(resCol)
                row += 1
            newData = {"numrows" : matrices[operand1]['numrows'],
                       "numcols" : matrices[operand1]['numcols'],
                       "matrixdata": resRow}
            name = calRequest['resultant']
            matrices.update({name:newData})
            return "AFTER " + calRequest['operationtype'].upper() + ": " + render_template("matrixTable.html", res = matrices[name]['matrixdata'],name=name), 200 # use html table to disply the data
        else: # prompt the error if the matrix cannot do add or subtracktion
            error = {}
            error.update({'datatype': 'status'})
            error.update({'statusmessage': "The number of columns and rows are not same, cannot do add or subtractions"})
            error.update({'errorcode': 12})
            return jsonify(error)

    # when the operation type is multiplication, use three loop to do the multiply
    elif calRequest['operationtype'] == 'multiplication':
        if matrices[operand1]['numcols'] == matrices[operand2]['numrows']:  # judge whether the matrices are eligible to do the multiplication
            numRow = 0
            resRow = []  #initialize the matrixdata for new matrix
            while numRow < matrices[operand1]['numrows']:
                numCol = 0
                resCol = [] #initialize each row of the matrix
                while numCol < matrices[operand2]['numcols']:
                    numSameRowCol = 0
                    eachNum = 0
                    while numSameRowCol < matrices[operand1]['numcols']:
                        eachNum += matrices[operand1]['matrixdata'][numRow][numSameRowCol] * matrices[operand2]['matrixdata'][numSameRowCol][numCol]
                        numSameRowCol += 1
                    resCol.append(eachNum)
                    numCol += 1
                resRow.append(resCol)
                numRow += 1
            newData = {"numrows" : matrices[operand1]['numrows'],
                       "numcols" : matrices[operand2]['numcols'],
                       "matrixdata": resRow}
            name = calRequest['resultant']
            matrices.update({name:newData})
            return "AFTER MULTIPLICATION: " + render_template("matrixTable.html", res=matrices[name]['matrixdata'], name=name), 200
        else: # prompt the error if the matrix cannot do multiplication
            error = {}
            error.update({'datatype': 'status'})
            error.update({'statusmessage': "The number of rows of the first matrix does not match the number of columns of the second matrix, can't do multiplication."})
            error.update({'errorcode': 12})
            return jsonify(error)


@app.errorhandler(404)
def page_not_found(e):
    '''
    Error Message when the entered url does not match records
    :param e: the error 
    :return: the error message
    '''
    error = {}
    error.update({'datatype': 'status'})
    error.update({
                  'statusmessage': "The page you found does not match, check your spell!!"})
    error.update({'errorcode': 404})
    return jsonify(error)

@app.errorhandler(405)
def request_wrong(e):
    '''
    Error message when the request does not match the server
    :param e: the error 
    :return: the error message
    '''
    error = {}
    error.update({'datatype': 'status'})
    error.update({
                  'statusmessage': "The request method does not match. Check the request."})
    error.update({'errorcode': 405})
    return jsonify(error)

@app.errorhandler(Exception)
def all_exception_handler(error):
    '''
    Error message catch all other exception
    :param error: the error
    :return: the error message
    '''
    error = {}
    error.update({'datatype': 'status'})
    error.update({
                  'statusmessage': "Server is down, please check your url and try again."})
    error.update({'errorcode': 500})
    return jsonify(error)

if __name__ == '__main__':
    app.run(debug=True,port=8080)