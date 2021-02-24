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
        if user_status=='logedIn':
            user_status = 'logedOut'
            get_db().execute("UPDATE UserSession SET status =?;" [user_status])
            get_db().commit()
        else:
            print("logIn First")
    except Exception as e:
        print(e)
        return False

def change_password(userToken, oldPassword, newPassword):
    user_status = get_db().execute("SELECT status FROM UserSession WHERE token =?;", [userToken])
    if user_status=='logedIn':
        oldPassword = get_db().execute("SELECT password FROM User WHERE password =?;", [password])
        if oldPassword == password:
            try:
                get_db().execute("UPDATE User SET password=?;", [password])
                get_db().commit()
            except Exception as e:
                print(e)
                return False

def get_user_data_by_token(userToken):
    try:
        user_profile = get_db().execute("SELECT u.* FROM User u inner join UserSession s on u.email = s.user_email  WHERE token =?;", [userToken])
        get_db().commit()
        return user_profile
    except Exception as e:
        print(e)
        return False


def get_user_data_by_email(userToken,userEmail):
    try:
        user_data = get_db().execute("SELECT u.email,u.first_name, u.last_name, u.city, u.country, u.gender FROM User u inner join UserSession s on u.email = s.user_email  WHERE token =?;", [userToken,userEmail])
        get_db().commit()
        return user_data
    except Exception as e:
        print(e)
        return False


def get_user_message_by_token(userToken):
    try:
        user_message = get_db().execute("SELECT p.post_message FROM Post p inner join UserSession s on p.user_email = s.user_email  WHERE token=?;", [userToken])
        get_db().commit()
        return user_message
    except Exception as e:
        print(e)
        return False

def get_user_message_by_email(userToken,userEmail):
    try:
        user_status = get_db().execute("SELECT status FROM UserSession WHERE token =?;", [userToken])
        if user_status=='logedin':
            user_message = get_db().execute("SELECT post_message FROM Post WHERE user_email =?;", [userEmail])
            get_db().commit()
            return user_message
        else:
            print("logIn First")
    except Exception as e:
        print(e)
        return False


def post_message(userToken, post_message, email):
    try:
        user_status = get_db().execute("SELECT status FROM UserSession WHERE token=? & user_email=?;", [userToken,email])
        if user_status == 'logedin':
            get_db().execute("INSERT INTO Post values(?,?);", [email,post_message])
        else:
            print("logIn to Post")
        get_db().commit()
        return user_post_message
    except Exception as e:
        print(e)
        return False




# def get_contact(name):
#     cursor = get_db().execute("select * from contact where name like ?", [name])
#     rows = cursor.fetchall()
#     cursor.close()
#     result = []
#     for index in range(len(rows)):
#         result.append({'name':rows[index][0], 'number':rows[index][1]})
#     return result
