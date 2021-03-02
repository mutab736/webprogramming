from flask import Flask, jsonify, request

import database_handler
import json
from uuid import uuid4

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
        try:
            result = database_handler.sign_up(data['email'], data['first_name'], data['last_name'], data['gender'], data['country'], data['city'], data['password'])
            if (result == True):
                return "", 201   # user created sucessfully
            else:
                return "", 500  #Something went wrong on database
        except Exception as e:
            if(str(e.args[0])=='UNIQUE constraint failed: User.email'):
                return "", 409   #Email already exist.
            else:
                return "", 500  #Something went wrong

    else:
        return "", 400 #Not good data.


@app.route('/signin', methods=['POST'])
def SignIn():
    data = request.get_json()
    if 'email' in data and 'password' in data:
        try:
            result = database_handler.sign_in(data['email'], data['password'])
            return jsonify({"token": result}), 200
        except Exception as e:
            print("e ",e)
            if(str(e.args[0])== 'Incorrect Password'):
                return "", 401 #Incorrect Password
            else:
                return "", 500 #Something went wrong.
    else:
        return "", 400 #Not good data

@app.route('/signout', methods=['GET'])
def SignOut():
    data = request.headers
    if 'Token' in data:
        print("token",data['Token'])
        result = database_handler.sign_out(data['Token'])
        if (result == True):
            return "", 200 #User Signout Sucessfully.
        else:
            return "", 401 #invalid token / Login First.
    else:
        return "", 400 #Not good data.


@app.route('/changepassword', methods=['POST'])
def ChangePassword():
    h_data = request.headers
    data = request.get_json()
    if 'Token' in h_data and 'oldPassword' in data and 'newPassword' in data:
        result = database_handler.change_password(h_data['Token'], data['oldPassword'], data['newPassword'])
        if (result == "success"):
            return "", 200 #Password Changed Sucessfully
        elif(result == "password is incorrect"):
            return "", 401 #Your Password is inncorrect
        elif(result == "Login First"):
            return "", 401  #You are logged out please login first.
        else:
            return "", 500 #Something went wrong

    else:
        return "", 400 #Not good data.

@app.route('/getuserdatabytoken', methods=['GET'])
def GetUserDataByTocken():
    data = request.headers
    if 'Token' in data:
        try:
            result = database_handler.get_user_data_by_token(data['Token'])
            x = {
                "email": result[0][0],
                "first_name": result[0][1],
                "last_name": result[0][2],
                "gender": result[0][3],
                "Country": result[0][4],
                "City": result[0][5]
                }
            result=json.dumps(x)
            return result, 200
        except Exception as e:
            print("something-", e)            
            return "", 401 #invalid token
    else:
        return "", 400 #Not good data

@app.route('/getuserdatabyemail', methods=['POST'])
def GetUserDataByEmail():
    h_data =request.headers
    data = request.get_json()
    if 'Token' in h_data and 'email' in data:
        try:
            result = database_handler.get_user_data_by_email(h_data['Token'], data['email'])

            x = {
                "email": result[0][0],
                "first_name": result[0][1],
                "last_name": result[0][2],
                "gender": result[0][3],
                "Country": result[0][4],
                "City": result[0][5]
                }
            result=json.dumps(x)
            return result, 200
    
        except Exception as e:
            if(str(e.args[0])=='invalid token / logIn First'):
                return "", 401 #Inavlid token / please login first.
            return "", 500 #Server side probelm

    else:
        return "", 400 #Not good data


@app.route('/getusermessagebytoken', methods=['GET'])
def GetUserMessageByToken():
    data = request.headers
    print("Data is: ", data)
    if 'Token' in data:
        try:
            result = database_handler.get_user_message_by_token(data['Token'])
            result = convert_resultset_to_Json(result)
     
            result=json.dumps(result)
            return result, 200
    
        except Exception as e:
            if(str(e.args[0])=='invalid token / logIn First'):
                return "", 401  #Inavlid token / please login first.
            elif (str(e.args[0])=='Token is Invalid'):
                return "", 401 #Tocken is Invalid.
            return "", 500  #Something went wrong.
    else:
        return "", 400 #Not good data


@app.route('/getusermessagebyemail', methods=['POST'])
def GetUserMessageByEmail():
    h_data = request.headers
    data = request.get_json()
    if 'Token' in h_data and 'email' in data:
        try:
            result = database_handler.get_user_message_by_email(h_data['Token'], data['email'])
            result = convert_resultset_to_Json(result)
            result=json.dumps(result)
            return result, 200
    
        except Exception as e:
            if(str(e.args[0])=='invalid token / logIn First'):
                return "", 401 #Inavlid token / please login first
            return "", 500 #Something went wrong
    else:
        return "", 400  #Not good data.


@app.route('/postmessage', methods=['POST'])
def PostMessage():
    h_data = request.headers
    data = request.get_json()
    if 'Token' in h_data and 'email' in data and 'message' in data:
        try:
            result = database_handler.post_message(h_data['Token'], data['email'], data['message'])
            
            return "", 200  #Message posted successfully
    
        except Exception as e:
            print("e is:",e)
            if(str(e.args[0])=='invalid token / logIn First'):
                return "", 401  #Inavlid token / please login first
            return "", 500 #Something went wrong.
    else:
        return "", 400 #Not good data


#util methods

def remove_dummy_chars_from_the_end_of_string(result):
    result=str(result)[2:(len(result)-4)]
    return result.strip()


def convert_resultset_to_Json(resultSet):
    json_array=[]
    for i in resultSet:
        print("i ",i)
        x = {
                "message": remove_dummy_chars_from_the_end_of_string(i)
                }
        json_array.append(x)
        return json_array



if __name__ == '__main__':
    app.run()
