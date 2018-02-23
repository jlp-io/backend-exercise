from flask import Flask, jsonify, request
import mockdb.mockdb_interface as db
import mockdb.dummy_data as dd
import json

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

"""
this is for part 1
@app.route('/users', methods=['GET'])
def partOne():
    return create_response(dd.initial_db_state
"""

@app.route('/users', methods=['GET', 'POST'])
def part134():
    if request.method == 'GET':
        team = request.args.get('team')
        data = dd.get('users')
        if team is None:
            matched = [i for i in data if i['team'] == team]
            return create_response({'users': matched})
        return create_response({'users': data})

    if request.method == 'POST':
        param = request.get_json()
        if param.get('name') or param.get('age') or param.get('team') is None:
            return create_response(status=404, message="Cannot be found")
        else:
            json = {'name': param.get('name'),
                'age': param.get('age'),
                'team': param.get('team')}
            return create_response(db.create('users', json))

@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def part256(id):
    if request.method == 'GET':
        if db.getbyId('users', int(id)) is None:
            return create_response(status=400, message="Not found")
        else:
            json = {
            'users': db.getId('users')
            }
            return create_response(json)

    if request.method == 'PUT':
        json = {'name': request.form['name'], 'age': request.form['age'], 'team': request.form['team']}
        if db.updateById('users', int(id), json) is None:
            return create_response(status=400, message="not found")
        else:
            return create_response(db.updateById('users', id, json))

    if request.method == 'DELETE':
        if db.getById('users', int(id)) is None:    
            return create_response(status=400, message="Not found")

        if db.getById('users', int(id)) is None:
            return create_response(None, 404, "User cannot be found")
        else:
            json = {
            'user': db.getById('users', int(id))
            }
        return create_response(json)

# TODO: Implement the rest of the API here!

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == '__main__':
    app.run(debug=True)