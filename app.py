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

@app.route('/users', methods = ['GET', 'POST'])
def users():
    if request.method == 'GET':
        if request.args.get('team') is None:
            data = {
                'users': db.get('users')
            }
        else:
            matched = [i for i in db.get('users') if i['team'] == request.args.get('team')]
            data = {
                'users': matched
            }
        return create_response(data)
    elif request.method == 'POST':
        input = request.get_json()
        payload = {'name': input.get('name'),
                   'age': input.get('age'),
                   'team': input.get('team')}
        return create_response(db.create('users', payload))

@app.route('/users/<id>', methods = ['GET', 'PUT', 'DELETE'])
def userById(id):
    if request.method == 'GET':
        if db.getById('users', int(id)) is None:
            return create_response(None, 404, "User cannot be found")
        else:
            data = {
                'user': db.getById('users', int(id))
            }
            return create_response(data)
    elif request.method == 'PUT':
        payload = {'name': request.form['name'], 'age': request.form['age'], 'team': request.form['team']}
        if db.updateById('users', int(id), payload) is None:
            return create_response(None, 404, "User cannot be found")
        else:
            return create_response(db.updateById('users', id, payload))
    elif request.method == 'DELETE':
        if db.getById('users', int(id)) is None:
            return create_response(None, 404, "User cannot be found")
        else:
            db.deleteById('users', int(id))
            return create_response({}, 200, "User deleted successfully")

# TODO: Implement the rest of the API here!

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == '__main__':
    app.run(debug=True)
