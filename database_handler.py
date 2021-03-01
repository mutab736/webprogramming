import sqlite3
from flask import g

DATABASE_URI = "D:\\sqlite3\\SQLiteStudio\\twidder"

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = sqlite3.connect(DATABASE_URI)
    return db

def disconnect_db():
    db = getattr(g, 'db', None)
    if db is not None:
        g.db.close()
        g.db = None

# def save_contact(name, number):
#     try:
#         get_db().execute("insert into contact values(?,?);", [name, number])
#         get_db().commit()
#         return True
#     except Exception as e:
#         print(e)
#         return False

def sign_in(email, password):
    try:
        get_db().execute("SELECT email, password FROM User WHERE email =?;", [email])
        get_db().commit()
        return True
    except Exception as e:
        print(e)
        return False


def sign_up(email, first_name, last_name, gender, city, country, password):
    try:
        print("Data1 is: ",email, first_name, last_name, gender, city, country, password)
        get_db().execute("insert into User (email, first_name, last_name, gender, city, country, password) values (?,?,?,?,?,?,?)", (email, first_name, last_name, gender, city, country, password))
        get_db().commit()
        return True
    except Exception as e:
        print(e)
        return False


def sign_out(userToken):
    try:
        user_status = get_db().execute("SELECT status FROM UserSession WHERE token =?;", [userToken])
        user_status = convert_cursor_with_single_value_to_string(user_status)
        user_status = str(user_status)
        if str(user_status)=='logedIn':
            user_status = 'logedOut'
            get_db().execute("UPDATE UserSession SET status ='"+user_status+"' where token ='"+userToken+"';")
            get_db().commit()    
            return True
        else:
            print("logIn First")
            return False
    except Exception as e:
        print(e)
        return False

def change_password(userToken, oldPassword, newPassword):
    user_status = get_db().execute("SELECT status FROM UserSession WHERE token =?;", [userToken])
    print("Test0")
    user_status = convert_cursor_with_single_value_to_string(user_status) #(user_status,2,len(user_status)-2)
    user_status = str(user_status)
    print("Test01", user_status)
    if str(user_status)=='logedIn':
        currentPassword = get_db().execute("SELECT password FROM User u inner join UserSession s on s.user_email=u.email WHERE token =?;", [userToken])
        currentPassword = convert_cursor_with_single_value_to_string(currentPassword) #(oldPassword, 2,len(oldPassword)-2)
        currentPassword = str(currentPassword)
        print("password and old password",currentPassword," - ", oldPassword)
        if oldPassword == currentPassword:
            print("Test1")
            try:
                print("Test2")
                get_db().execute("UPDATE User SET password=?;", [newPassword])
                print("Test3")
                get_db().commit()
                print("Test4")
                return "success"
            except Exception as e:
                print(e)
                return False
        else:
            return "password is incorrect"
    else:
        return "Login First"

def get_user_data_by_token(userToken):
    try:
        user_profile = get_db().execute("SELECT u.* FROM User u inner join UserSession s on u.email = s.user_email  WHERE token =?;", [userToken])
        #get_db().commit()
        print("user profile ",user_profile)
        #user_profile = convert_cursor_with_single_record_to_user_info_json(user_profile)
        #user_profile = user_profile.fetchall()
        #user_profile = json.dumps(user_profile)#convert_cursor_with_single_record_to_json(user_profile)
        print("user profile info ",user_profile)
        return user_profile.fetchall()
    except Exception as e:
        print(e)
        return False


def get_user_data_by_email(userToken,userEmail):
    try:
        user_status = check_token_validaty(userToken)
        if str(user_status)=='logedIn':
            print("some line1")
            # user_data = get_db().execute("SELECT u.email,u.first_name, u.last_name, u.city, u.country, u.gender FROM User u inner join UserSession s on u.email = s.user_email  WHERE token =?;", [userToken,userEmail])
            user_data = get_db().execute("SELECT u.email,u.first_name, u.last_name, u.city, u.country, u.gender FROM User u WHERE u.email =?;", [userEmail])
            print("some line2")
            # get_db().commit()
            return user_data.fetchall()
        elif str(user_status)=='logedOut':
            print("logIn First")
            #return "logIn First"
            raise Exception("logIn First")
        else:
            raise Exception("Token is Invalid")

    except Exception as e:
        print(e)
        raise Exception(e)


def get_user_message_by_token(userToken):
    try:
        user_status = check_token_validaty(userToken)
        if str(user_status)=='logedIn':
            user_message = get_db().execute("SELECT p.post_message FROM Post p inner join UserSession s on p.user_email = s.user_email  WHERE token=?;", [userToken])
            # get_db().commit()
            return user_message.fetchall()
        elif str(user_status)=='logedOut':
            print("logIn First")
            #return "logIn First"
            raise Exception("logIn First")
        else:
            raise Exception("Token is Invalid")
    except Exception as e:
        print(e)
        raise Exception(e)

def get_user_message_by_email(userToken,userEmail):
    try:
        user_status = check_token_validaty(userToken)
        print("status ",user_status)
        if str(user_status)=='logedIn':
            user_message = get_db().execute("SELECT post_message FROM Post WHERE user_email =?;", [userEmail])
            # get_db().commit()
            print("user status",user_status)
            return user_message.fetchall()
        elif str(user_status)=='logedOut':
            print("logIn First")
            #return "logIn First"
            raise Exception("logIn First")
        else:
            print("U-S", user_status)
            raise Exception("Token is Invalid")
    except Exception as e:
        print(e)
        raise Exception(e)


def post_message(userToken, email,post_message,):
    try:
        print("token",userToken,"email",email)
        user_status = get_db().execute("SELECT status FROM UserSession WHERE token=? and user_email=?;", [userToken,email])        
        user_status = convert_cursor_with_single_value_to_string(user_status)
        user_status = str(user_status)
        print("User Status: ", user_status)
        if user_status == 'logedIn':
            get_db().execute("INSERT INTO Post(user_email,post_message) values(?,?);", [email,post_message])
            get_db().commit()
            return True;
        elif str(user_status)=='logedOut':
            print("logIn First")
            #return "logIn First"
            raise Exception("logIn First")
        else:
            print("U-S", user_status)
            raise Exception("Token is Invalid")
    except Exception as e:
        print(e)
        raise Exception(e)

def convert_cursor_with_single_value_to_string(cursor,start,end):
    fetch = cursor.fetchall()
    result = str(fetch[0])
    result=str(result)[start:end]
    return result

def convert_cursor_with_single_value_to_string(cursor):
    fetch = cursor.fetchall()
    print("strFetch: ",len(str(fetch)))
    if len(str(fetch))==2:
        return "invalid token"
    result = str(fetch[0])
    print("here ",len(result))
    result=str(result)[2:(len(result)-3)]
    return result.strip()

def check_token_validaty(token):
    token_status = get_db().execute("SELECT status FROM UserSession WHERE token =?;", [token])
    print("Test0")
    token_status = convert_cursor_with_single_value_to_string(token_status) #(user_status,2,len(user_status)-2)
    token_status = str(token_status)
    print("Test01", token_status)
    return token_status
     

#def convert_cursor_with_single_record_to_user_info_json(cursor):
    # user_profile = cursor.fetchall()
    # print("email ",str(user_profile[0][0]))
    #  result = "{\"email\":\""+user_profile[0][0]+"\","
    #  result += "\"first_name\":\""+user_profile[0][1]+"\","
    #  result += "\"last_name\":\""+user_profile[0][2]+"\","
    #  result += "\"country\":\""+user_profile[0][3]+"\","
    #  result += "\"city\":\""+user_profile[0][4]+"\","
    #  result += "\"geneder\":\""+user_profile[0][5]+"\","
    #  result += "\"telephone\":\""+user_profile[0][6]+"\"}"
    #  print("result is ",result)

    #  result = ""{email:""+user_profile[0][0]+"","
    #  result += ""first_name":""+user_profile[0][1]+"","
    #  result += ""last_name":""+user_profile[0][2]+"","
    #  result += ""country":""+user_profile[0][3]+"","
    #  result += ""city":""+user_profile[0][4]+"","
    #  result += ""geneder":""+user_profile[0][5]+"","
    #  result += ""telephone":""+user_profile[0][6]+""}"
    #  print("result is ",result)
    #  return result

    #  for i in user_profile:
    #      print("email",i)




#def convert_cursor_with_single_record_to_json(cursor):
    



# def get_contact(name):
#     cursor = get_db().execute("select * from contact where name like ?", [name])
#     rows = cursor.fetchall()
#     cursor.close()
#     result = []
#     for index in range(len(rows)):
#         result.append({'name':rows[index][0], 'number':rows[index][1]})
#     return result
