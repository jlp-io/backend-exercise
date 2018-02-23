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
@app.route('/users', methods=['GET'])
def users():
    team = request.args.get('team')
    if not team:
        data = {
            'users': db.get('users')
        }
        return create_response(data)
    users = db.get('users')
    team_users = [u for u in users if u['team'] == team]
    data = {
        'users': team_users
    }
    return create_response(data)


@app.route('/users/<id>', methods=['GET'])
def users_id(id):
    user = db.getById('users', int(id))
    if not user:
        return create_response({}, 404, "no such user")
    data = {
        'user': user
    }
    return create_response(data)

@app.route('/users', methods=['POST'])
def post_user():
    json = request.get_json()
    if not json or 'name' not in json or 'age' not in json or 'team' not in json:
        return create_response({}, 422, "specify name, age, team of new user")
    user_data = {'name': json['name'], 'age': json['age'],'team': json['team']}
    data = db.create('users',user_data)
    return create_response(data, 201)

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    json = request.get_json()
    data = {}
    if json:
        if 'name' in json:
            data['name'] = json['name']
        if 'age' in json:
            data['age'] = json['age']
        if 'team' in json:
            data['team'] = json['team']
    user = db.updateById('users', int(id), data)
    if not user:
        return create_response({}, 404, "no such user")
    return create_response(user, 201) 
"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == '__main__':
    app.run(debug=True)
