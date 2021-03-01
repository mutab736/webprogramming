from flask import Flask, jsonify, request

import database_handler
import json

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
        # print("Data is: ", data)
        #if len(data['name']) < 50 and len(data['number']) < 50:
        if 1==1:
            result = database_handler.sign_up(data['email'], data['first_name'], data['last_name'], data['gender'], data['country'], data['city'], data['password'])
            if (result == True):
                return jsonify({"msg": "User Created Successfully"}), 200
            else:
                return jsonify({"msg": "Something went wrong."}), 500
        else:
            return jsonify({"msg": "Not good data."}), 400
    else:
        return jsonify({"msg": "Not good data."}), 400


@app.route('/signin', methods=['POST'])
def SignIn():
    data = request.get_json()
    if 'email' in data and 'password' in data:
        result = database_handler.sign_in(data['email'], data['password'])
        if (result == True):
            return jsonify({"msg": "User Signin Sucessfully."}), 200
        else:
            return jsonify({"msg": "Something went wrong."}), 500
    else:
        return jsonify({"msg": "Not good data."}), 400

@app.route('/signout', methods=['GET'])
def SignOut():
    data = request.headers #request.get_json()
    print("data",data)
    if 'Token' in data:
        print("token",data['Token'])
        result = database_handler.sign_out(data['Token'])
        if (result == True):
            return jsonify({"msg": "User Signout Sucessfully."}), 200
        else:
            return jsonify({"msg": "Something went wrong."}), 500
    else:
        return jsonify({"msg": "Not good data."}), 400


@app.route('/changepassword', methods=['POST'])
def ChangePassword():
    h_data = request.headers
    data = request.get_json()
    if 'Token' in h_data and 'oldPassword' in data and 'newPassword' in data:
        result = database_handler.change_password(h_data['Token'], data['oldPassword'], data['newPassword'])
        print("Data is: ",data)
        if (result == "success"):
            return jsonify({"msg": "Password Changed Sucessfully."}), 200
        elif(result == "password is incorrect"):
            return jsonify({"msg": "Your Password is inncorrect."}), 401
        elif(result == "Login First"):
            return jsonify({"msg": "You are logged out please login first."}), 401
        else:
            return jsonify({"msg": "Something went wrong."}), 500

    else:
        return jsonify({"msg": "Not good data."}), 400

@app.route('/getuserdatabytoken', methods=['GET'])
def GetUserDataByTocken():
    data = request.headers #request.get_json()
    if 'Token' in data:
        try:
            result = database_handler.get_user_data_by_token(data['Token'])
            print("result is: ",result)
            # if (result == "success"):
            #     return jsonify(), 200
            # elif(result == "password is incorrect"):
            #     return jsonify({"msg": "Your Password is inncorrect."}), 200
            # elif(result == "Login First"):
            #     return jsonify({"msg": "You are logged out please login first."}), 200
            # else:
            #     return jsonify({"msg": "Something went wrong."}), 500
            print("getuserinfo 1", result[0][0])

            x = {
                "email": result[0][0],
                "first_name": result[0][1],
                "last_name": result[0][2],
                "gender": result[0][3],
                "Country": result[0][4],
                "City": result[0][5]
                }
            print("getuserinfo 2")
            result=json.dumps(x)
            print("Result is: ", result)
            return result, 200
    
        except Exception as e:
            print("Exception is: ", e)
            return jsonify({"msg": "Something went wrong."}), 500

    else:
        return jsonify({"msg": "Not good data."}), 400

@app.route('/getuserdatabyemail', methods=['POST'])
def GetUserDataByEmail():
    h_data =request.headers
    data = request.get_json()
    print("Data is: ", data)
    if 'Token' in h_data and 'email' in data:
        try:
            result = database_handler.get_user_data_by_email(h_data['Token'], data['email'])
            print("result is: ",result)
            # if (result == "success"):
            #     return jsonify(), 200
            # elif(result == "password is incorrect"):
            #     return jsonify({"msg": "Your Password is inncorrect."}), 200
            # elif(result == "Login First"):
            #     return jsonify({"msg": "You are logged out please login first."}), 200
            # else:
            #     return jsonify({"msg": "Something went wrong."}), 500
            print("getuserinfo 1", result[0][0])

            x = {
                "email": result[0][0],
                "first_name": result[0][1],
                "last_name": result[0][2],
                "gender": result[0][3],
                "Country": result[0][4],
                "City": result[0][5]
                }
            print("getuserinfo 2")
            result=json.dumps(x)
            print("Result is: ", result)
            return result, 200
    
        except Exception as e:
            print("Exception is: ", e," ",e.args[0])
            if(str(e.args[0])=='logIn First'):
                print("test haha")
                return jsonify({"msg": "you are not loggdin please login first."}), 401
            return jsonify({"msg": "Something went wrong."}), 500

    else:
        return jsonify({"msg": "Not good data."}), 400


@app.route('/getusermessagebytoken', methods=['GET'])
def GetUserMessageByToken():
    data = request.headers #request.get_json()
    print("Data is: ", data)
    if 'Token' in data:
        try:
            result = database_handler.get_user_message_by_token(data['Token'])
            print("result is: ",result)
            result = convert_resultset_to_Json(result)
            # if (result == "success"):
            #     return jsonify(), 200
            # elif(result == "password is incorrect"):
            #     return jsonify({"msg": "Your Password is inncorrect."}), 200
            # elif(result == "Login First"):
            #     return jsonify({"msg": "You are logged out please login first."}), 200
            # else:
            #     return jsonify({"msg": "Something went wrong."}), 500
            #print("getuserinfo 1", result[0][0])
     
            print("getuserinfo 2 ",result)
            result=json.dumps(result)
            print("Result is: ", result)
            return result, 200
    
        except Exception as e:
            print("Exception is: ", e)
            if(str(e.args[0])=='logIn First'):
                print("test haha")
                return jsonify({"msg": "you are not loggdin please login first."}), 401
            elif (str(e.args[0])=='Token is Invalid'):
                return jsonify({"msg": "Tocken is Invalid."}), 401
            return jsonify({"msg": "Something went wrong."}), 500
    else:
        return jsonify({"msg": "Not good data."}), 400


@app.route('/getusermessagebyemail', methods=['POST'])
def GetUserMessageByEmail():
    h_data = request.headers
    data = request.get_json()
    print("Data is: ", data)
    if 'Token' in h_data and 'email' in data:
        try:
            result = database_handler.get_user_message_by_email(h_data['Token'], data['email'])
            print("result is: ",result)
            result = convert_resultset_to_Json(result)
            # if (result == "success"):
            #     return jsonify(), 200
            # elif(result == "password is incorrect"):
            #     return jsonify({"msg": "Your Password is inncorrect."}), 200
            # elif(result == "Login First"):
            #     return jsonify({"msg": "You are logged out please login first."}), 200
            # else:
            #     return jsonify({"msg": "Something went wrong."}), 500
            #print("getuserinfo 1", result[0][0])
     
            print("getuserinfo 2 ",result)
            result=json.dumps(result)
            print("Result is: ", result)
            return result, 200
    
        except Exception as e:
            print("Exception is: ", e)
            if(str(e.args[0])=='logIn First'):
                print("test haha")
                return jsonify({"msg": "you are not loggdin please login first."}), 401
            elif (str(e.args[0])=='Token is Invalid'):
                return jsonify({"msg": "Tocken is Invalid."}), 401
            return jsonify({"msg": "Something went wrong."}), 500
    else:
        return jsonify({"msg": "Not good data."}), 400


@app.route('/postmessage', methods=['POST'])
def PostMessage():
    h_data = request.headers
    data = request.get_json()
    print("Data is: ", data)
    if 'Token' in h_data and 'email' in data and 'message' in data:
        try:
            result = database_handler.post_message(h_data['Token'], data['email'], data['message'])
            #print("result is: ",result)
            #result = convert_resultset_to_Json(result)
            # if (result == "success"):
            #     return jsonify(), 200
            # elif(result == "password is incorrect"):
            #     return jsonify({"msg": "Your Password is inncorrect."}), 200
            # elif(result == "Login First"):
            #     return jsonify({"msg": "You are logged out please login first."}), 200
            # else:
            #     return jsonify({"msg": "Something went wrong."}), 500
            #print("getuserinfo 1", result[0][0])
     
            #print("getuserinfo 2 ",result)
            #result=json.dumps(result)
            #print("Result is: ", result)
            return jsonify({"msg": "message posted successfully."}), 200
    
        except Exception as e:
            print("Exception is: ", e)
            if(str(e.args[0])=='logIn First'):
                print("test haha")
                return jsonify({"msg": "you are not loggdin please login first."}), 401
            elif (str(e.args[0])=='Token is Invalid'):
                return jsonify({"msg": "Tocken is Invalid."}), 401
            return jsonify({"msg": "Something went wrong."}), 500
    else:
        return jsonify({"msg": "Not good data."}), 400


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
    for i in json_array:
        print("jsonArray ",i)
    return json_array
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
