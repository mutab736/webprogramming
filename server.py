from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError

from flask import Flask, jsonify, request
app = Flask(__name__, static_url_path='')
app.debug = True

import database_handler
import json
from uuid import uuid4


@app.route('/')
def root():
    return app.send_static_file('client.html')
    #return jsonify({'response':'Welcome to TDDD97'})

@app.teardown_request
def after_request(exception):
    database_handler.disconnect_db()

sockets = dict()
# @app.route("/api")
# def api():
#     if request.environ.get('wsgi.websocket'):
#         print(sockets)
#         ws = request.environ['wsgi.websocket']
#         jsonString = ws.receive()
#         jsonResult = json.loads(jsonString)
#         token = jsonResult['userToken']
#         email = database_helper.get_user_email_by_token(token)
#         if email in sockets:
#             sockets[email].send("true")
#         sockets[email] = ws
#         while True:
#             try:
#                 result = ws.receive()
#             except:
#                 for email in sockets.keys():
#                     if sockets[email] == ws:
#                         del sockets[email]
#                 break
#     return "socket closed"

@app.route('/socket')
def web_socket():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        obj = ws.receive()
        data = json.loads(obj)

        try:
            print("Data",data)
            sockets[data['email']] = ws

            while True:
                obj = ws.receive()
                #print("ws recive",obj)
                if obj is None:
                    del sockets[data['email']]
                    ws.close()
                    return ""

        except WebSocketError as e:
            del sockets[data['email']]

    return ""


@app.route('/signup', methods=['POST'])
def SignUp():
    data = request.get_json()
    if 'email' in data and 'firstname' in data and 'familyname' in data and 'gender' in data and 'country' in data and 'city' in data and 'password' in data:
        try:
            result = database_handler.sign_up(data['email'], data['firstname'], data['familyname'], data['gender'], data['country'], data['city'], data['password'])
            if (result == True):
                return "", 201   #User created sucessfully
            else:
                return "", 500  #Something went wrong on database
        except Exception as e:
            if(str(e.args[0])=='UNIQUE constraint failed: User.email'):
                return "", 409   #Email already exist.
            else:
                return "", 500  #Something went wrong

    else:
        return "", 400 #Not good data.


# @app.route('/signin', methods=['POST'])
# def SignIn():
#     data = request.get_json()
#     if 'email' in data and 'password' in data:
#         try:
#             result = database_handler.sign_in(data['email'], data['password'])
#             return jsonify({"token": result}), 200
#         except Exception as e:
#             print("e ",e)
#             if(str(e.args[0])== 'Incorrect Password'):
#                 return "", 401 #Incorrect Password
#             else:
#                 return "", 500 #Something went wrong.
#     else:
#         return "", 400 #Not good data

@app.route('/signin', methods=['POST'])
def SignIn():
    data = request.get_json()
    if 'email' in data and 'password' in data:
        try:
            is_user_loggedIn(data['email'])
            print("try sigin")
            result = database_handler.sign_in(data['email'], data['password'])
            #is_user_loggedIn(data['email'])
            return jsonify({"token": result}), 200
        except Exception as e:
            if(str(e.args[0])== 'Incorrect Password'):
                return "", 401 #Incorrect Password
            else:
                return "", 500 #Something went wrong.
    else:
        return "", 400 #Not good data

@app.route('/signout', methods=['GET'])
def SignOut():
    data = request.headers
    print("Token ",data['Token'])
    if 'Token' in data:
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
            return "", 201 #Password Changed Sucessfully
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
            if(len(result)==2):
                return jsonify(""),204
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
    print("posted message data ",h_data," ",data)
    if 'Token' in h_data and 'email' in data and 'message' in data:
        try:
            result = database_handler.post_message(h_data['Token'], data['email'], data['message'])
            
            return "", 201  #Message posted successfully
    
        except Exception as e:
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
        x = {
                "message": remove_dummy_chars_from_the_end_of_string(i)
                }
        json_array.append(x)
    return json_array

def is_user_loggedIn(userEmail):
    loggedIn = database_handler.get_session_status_by_email(userEmail)
    print("Loggedin ",loggedIn)
    if loggedIn ==True:
        if userEmail in sockets:
            try:
                ws = sockets[userEmail]
                ws.send(json.dumps({'success': False, 'message': 'You have been logged out'}))
            except WebSocketError as e:
                del sockets[userEmail]
            database_handler.deactivate_session_status(userEmail)#remove_logged_in_user(database_helper.get_logged_in_user_by_email(email)[1])


if __name__ == '__main__':
    http_server = WSGIServer(('',5001), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    #app.run()
