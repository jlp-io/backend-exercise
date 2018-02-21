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
@app.route('/users')
def get_all_users():
    team_name = request.args.get('team')
    if team_name == None:
        data = {
            'users': db.get('users')
        }
        return create_response(data)
    all_users = db.get('users')
    matched_users = [user for user in all_users if user['team'] == team_name]
    data = {'users': matched_users}
    return create_response(data)

@app.route('/users/<id>')
def get_user_by_id(id):
    user = db.getById('users', int(id))
    if user == None:
        return create_response({}, 404, 'user not found')
    return create_response(user)

@app.route('/users', methods=['POST'])
def post_user():
    request_json = request.get_json()
    data = {}
    try:
        payload = {'name': request_json['name'], 'age':request_json['age'], 'team': request_json['team']}
        data = db.create('users', payload)
        return create_response(data, status=201)
    except:
        return create_response(data, 422, 'user name, age and team must be provided')

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):    
    request_json = request.get_json()
    data = {}

    try:
        data['name'] = request_json['name']
    except:
        pass
    try:
        data['age'] = request_json['age']
    except:
        pass
    try:
        data['team'] = request_json['team']
    except:
        pass

    response = db.updateById('users', int(id), data)
    if response == None:
        return create_response({}, 404, 'user not found')
    return create_response(response, 201)

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):  
    users =  db.getById('users', int(id))
    if users == None:
        return create_response({}, 404, 'user not found')
    db.deleteById('users', int(id))
    return create_response({}, 200, 'delete success')
    

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == '__main__':
    app.run(debug=True)
