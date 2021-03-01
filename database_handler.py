import sqlite3
from flask import g
from uuid import uuid4


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


def sign_in(email, password):
    # try:
    #     #get_db().execute("SELECT email, password FROM User WHERE email =?;", [email])
    #     currentPassword = get_db().execute("SELECT password FROM User WHERE email =?;", [email])
    #     # get_db().commit()
    #     currentPassword = convert_cursor_with_single_value_to_string(currentPassword)
    #     currentPassword = str(currentPassword)
    #     if password == currentPassword:
    #         rand_token = uuid4()
    #         get_db().execute("insert into UserSession(token,email) values (?,?);", (rand_token,email))
    #         get_db().commit()
    #         return rand_token
    #     else:
    #        raise Exception('Incorrect Password')
    # except Exception as e:
    #     print(e)
    #     raise Exception(e)
    # get_db().execute("SELECT email, password FROM User WHERE email =?;", [email])
    currentPassword = get_db().execute(
        "SELECT password FROM User WHERE email =?;", [email])
    currentPassword = convert_cursor_with_single_value_to_string(
        currentPassword)
    currentPassword = str(currentPassword)
    if password == currentPassword:
        rand_token = str(uuid4())
        # just get the first part of the generated token,so instead of (XXXXXX-XXXXXX-XXXXX-XXXX)
        # we get the first part only
        rand_token = rand_token[0:rand_token.find("-")]
        print("token ", rand_token)
        status = "logedIn"
        get_db().execute("insert into UserSession(token,user_email,status) values (?,?,?);",
               (rand_token, email, status))
        get_db().commit()
        return rand_token
    else:
        raise Exception('Incorrect Password')


def sign_up(email, first_name, last_name, gender, city, country, password):
    # try:
    #     get_db().execute("insert into User (email, first_name, last_name, gender, city, country, password) values (?,?,?,?,?,?,?)", (email, first_name, last_name, gender, city, country, password))
    #     get_db().commit()
    #     return True
    # except Exception as e:
    #     print(e)
    #     raise Exception(e)

    get_db().execute("insert into User (email, first_name, last_name, gender, city, country, password) values (?,?,?,?,?,?,?)",
           (email, first_name, last_name, gender, city, country, password))
    get_db().commit()
    return True


def sign_out(userToken):
    # try:
    #     user_status = get_db().execute("SELECT status FROM UserSession WHERE token =?;", [userToken])
    #     user_status = convert_cursor_with_single_value_to_string(user_status)
    #     user_status = str(user_status)
    #     if str(user_status)=='logedIn':
    #         user_status = 'logedOut'
    #         get_db().execute("UPDATE UserSession SET status ='"+user_status+"' where token ='"+userToken+"';")
    #         get_db().commit()
    #         return True
    #     else:
    #         print("logIn First")
    #         return False
    # except Exception as e:
    #     print(e)
    #     return False

    user_status = get_db().execute(
        "SELECT status FROM UserSession WHERE token =?;", [userToken])
    user_status = convert_cursor_with_single_value_to_string(user_status)
    user_status = str(user_status)
    if str(user_status) == 'logedIn':
        user_status = 'logedOut'
        get_db().execute("UPDATE UserSession SET status ='" +
               user_status+"' where token ='"+userToken+"';")
        get_db().commit()
        return True
    else:
        print("logIn First")
        return False


def change_password(userToken, oldPassword, newPassword):
    user_status = get_db().execute(
        "SELECT status FROM UserSession WHERE token =?;", [userToken])
    user_status = convert_cursor_with_single_value_to_string(user_status)
    user_status = str(user_status)
    if str(user_status) == 'logedIn':
        currentPassword = get_db().execute(
            "SELECT password FROM User u inner join UserSession s on s.user_email=u.email WHERE token =?;", [userToken])
        currentPassword = convert_cursor_with_single_value_to_string(
            currentPassword)
        currentPassword = str(currentPassword)
        if oldPassword == currentPassword:
            try:
                get_db().execute("UPDATE User SET password=?;", [newPassword])
                get_db().commit()
                return "success"
            except Exception as e:
                return False
        else:
            return "password is incorrect"
    else:
        return "Login First"


def get_user_data_by_token(userToken):
    # try:
    user_status = check_token_validaty(userToken)
    if str(user_status) == 'logedIn':
        user_profile = get_db().execute(
            "SELECT u.* FROM User u inner join UserSession s on u.email = s.user_email  WHERE token =?;", [userToken])
        return user_profile.fetchall()
    elif str(user_status) == 'logedOut':
        print("logIn First")
        raise Exception("invalid token / logIn First")
    # except Exception as e:
    #    raise Exception(e)


def get_user_data_by_email(userToken, userEmail):
    # try:
    user_status = check_token_validaty(userToken)
    if str(user_status) == 'logedIn':
        user_data = get_db().execute("SELECT u.email,u.first_name, u.last_name, u.city, u.country, u.gender FROM User u WHERE u.email =?;", [userEmail])
        return user_data.fetchall()
    # elif str(user_status)=='logedOut':
    #     print("logIn First")
    #     raise Exception("logIn First")
    else:
        raise Exception("invalid token / logIn First")

    # except Exception as e:
    #     raise Exception(e)


def get_user_message_by_token(userToken):
    # try:
    user_status = check_token_validaty(userToken)
    if str(user_status)=='logedIn':
        user_message = get_db().execute("SELECT p.post_message FROM Post p inner join UserSession s on p.user_email = s.user_email  WHERE token=?;", [userToken])
        return user_message.fetchall()
    # elif str(user_status)=='logedOut':
    #     print("logIn First")
    #     raise Exception("invalid token / logIn First")
    else:
        raise Exception("invalid token / logIn First")
    # except Exception as e:
    #     raise Exception(e)

def get_user_message_by_email(userToken,userEmail):
    # try:
    user_status = check_token_validaty(userToken)
    print("status ",user_status)
    if str(user_status)=='logedIn':
        user_message = get_db().execute("SELECT post_message FROM Post WHERE user_email =?;", [userEmail])
        return user_message.fetchall()
    # elif str(user_status)=='logedOut':
    #     print("logIn First")
    else:
        raise Exception("invalid token / logIn First")
    # else:
    #     raise Exception("Token is Invalid")
    # except Exception as e:
    #     raise Exception(e)


def post_message(userToken, email,post_message,):
    # try:
    user_status = get_db().execute("SELECT status FROM UserSession WHERE token=? and user_email=?;", [userToken,email])        
    user_status = convert_cursor_with_single_value_to_string(user_status)
    user_status = str(user_status)
    if user_status == 'logedIn':
        get_db().execute("INSERT INTO Post(user_email,post_message) values(?,?);", [email,post_message])
        get_db().commit()
        return True;
    # elif str(user_status)=='logedOut':
    #     raise Exception("logIn First")
    else:
        raise Exception("invalid token / logIn First")
    # except Exception as e:
    #     raise Exception(e)

# util methods
# def convert_cursor_with_single_value_to_string(cursor,start,end):
#     fetch = cursor.fetchall()
#     result = str(fetch[0])
#     result=str(result)[start:end]
#     return result

def convert_cursor_with_single_value_to_string(cursor):
    fetch = cursor.fetchall()
    if len(str(fetch))==2:
        return "invalid token"
    result = str(fetch[0])
    result=str(result)[2:(len(result)-3)]
    return result.strip()

def check_token_validaty(token):
    token_status = get_db().execute("SELECT status FROM UserSession WHERE token =?;", [token])
    token_status = convert_cursor_with_single_value_to_string(token_status)
    token_status = str(token_status)
    return token_status
