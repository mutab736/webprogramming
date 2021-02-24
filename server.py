from flask import Flask, jsonify, request

import database_handler

app = Flask(__name__)
app.debug = True

@app.route('/')
def root():
    return jsonify({'response':'Welcome to TDDD97'})

@app.teardown_request
def after_request(exception):
    database_handler.disconnect_db()

@app.route('/signup', methods=['POST'])
def SignUp():
    data = request.get_json()
    if 'email' in data and 'first_name' in data and 'last_name' in data and 'gender' in data and 'country' in data and 'city' in data and 'password' in data:
        print("Data is: ", data)
        #if len(data['name']) < 50 and len(data['number']) < 50:
        if 1==1:
            result = database_handler.save_user(data['email'], data['first_name'], data['last_name'], data['gender'], data['country'], data['city'], data['password'])
            if (result == True):
                return jsonify({"msg": "User Created Successfully"}), 200
            else:
                return jsonify({"msg": "Something went wrong."}), 500
        else:
            return jsonify({"msg": "Not good data."}), 400
    else:
        return jsonify({"msg": "Not good data."}), 400


@app.route('/signin', methods=['POST'])
def SignIn(userEmail,password):
    data = request.get_json()
    if 'email' in data and 'password' in data:
        result = database_handler.save_user(data['email'], data['first_name'], data['last_name'], data['gender'], data['country'], data['city'], data['password'])
        if (result == True):
            return jsonify({"msg": "User Signin Sucessfully."}), 200
        else:
            return jsonify({"msg": "Something went wrong."}), 500
    else:
        return jsonify({"msg": "Not good data."}), 400




# @app.route('/contact/save1', methods=['POST'])
# def save_contact1():
#     data = request.get_json()
#     if 'name' in data and 'number' in data:
#         if len(data['name']) < 50 and len(data['number']) < 50:
#             result = database_handler.save_contact(data['name'], data['number'])
#             if (result == True):
#                 return jsonify({"msg": "Contact saved."}), 200
#             else:
#                 return jsonify({"msg": "Something went wrong."}), 500
#         else:
#             return jsonify({"msg": "Not good data."}), 400
#     else:
#         return jsonify({"msg": "Not good data."}), 400


# @app.route('/contact/find/<name>', methods=['GET'])
# def find_contact(name):
#     if name is not None:
#         contacts = database_handler.get_contact(name)
#         if contacts is not None:
#             if len(contacts) == 0:
#                 return jsonify([]), 404
#             else:
#                 return jsonify(contacts), 200
#         else:
#             return jsonify([]), 404


if __name__ == '__main__':
    app.run()
