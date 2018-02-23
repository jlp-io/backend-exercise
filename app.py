from flask import Flask, jsonify, request
import mockdb.mockdb_interface as db

app = Flask(__name__)

def create_response(data={}, status=200, message=''):
    """
    Wraps response in a consistent format throughout the API
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response

    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself
    """
    response = {
        'success': 200 <= status < 300,
        'code': status,
        'message': message,
        'result': data
    }
    return jsonify(response), status

"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""

@app.route('/')
def hello_world():
    return create_response('hello world!')

@app.route('/mirror/<name>')
def mirror(name):
    data = {
        'name': name
    }
    return create_response(data)



# TODO: Implement the rest of the API here!


@app.route('/users', methods = ['GET'])
def users():
    if ('team' in request.args):
        team = request.args.get('team')
        data = db.get('users')
        ret = []
        for item in data:
            if (item['team'] == team):
                ret.append(item)

        return create_response(ret)
    else:
        data = db.get('users')
        return create_response(data)

@app.route('/users/<userID>', methods = ['GET'])
def usersID(userID):
    data = db.get('users')
    if (int(userID) > len(data) or int(userID) <= 0):
        return create_response({}, 404, 'No such user exists!')
    else:
        user = data[int(userID)-1]
        return create_response(user)

@app.route('/users', methods = ['POST'])
def createUser():
    if all(k in request.get_json() for k in ('team', 'name', 'age')):
        newUser = request.get_json()
        print(newUser)
        createdUser = db.create('users', newUser)
        return create_response(createdUser, 201, 'User created successfully')
    else:
        return create_response({}, 422, 'User was not created!')




"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == '__main__':
    app.run(debug=True)
