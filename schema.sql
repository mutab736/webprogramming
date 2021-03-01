--
-- File generated with SQLiteStudio v3.2.1 on Mon Mar 1 10:40:59 2021
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: contact
CREATE TABLE contact (
    name   VARCHAR (30) NOT NULL,
    number INTEGER (10) NOT NULL
);


-- Table: Post
CREATE TABLE Post (
    id           INTEGER       PRIMARY KEY,
    user_email   VARCHAR (255) REFERENCES User (email),
    post_message VARCHAR (255) NOT NULL
);

INSERT INTO Post (
                     id,
                     user_email,
                     post_message
                 )
                 VALUES (
                     1,
                     'talha@abc.com',
                     'Message1'
                 );

INSERT INTO Post (
                     id,
                     user_email,
                     post_message
                 )
                 VALUES (
                     2,
                     'talha@abc.com',
                     'Message2'
                 );

INSERT INTO Post (
                     id,
                     user_email,
                     post_message
                 )
                 VALUES (
                     3,
                     'talha@abc.com',
                     'Message3'
                 );


-- Table: User
CREATE TABLE User (
    email      VARCHAR (100) PRIMARY KEY,
    first_name VARCHAR (100) NOT NULL,
    last_name  VARCHAR (100) NOT NULL,
    city       VARCHAR (50)  NOT NULL,
    country    VARCHAR (50)  NOT NULL,
    gender     VARCHAR (10)  CHECK (gender = 'male' OR 
                                    'female') 
                             NOT NULL,
    password   VARCHAR (255) NOT NULL
);

INSERT INTO User (
                     email,
                     first_name,
                     last_name,
                     city,
                     country,
                     gender,
                     password
                 )
                 VALUES (
                     'email',
                     'first_name',
                     'last_name',
                     'city',
                     'country',
                     'male',
                     '1234567890'
                 );

INSERT INTO User (
                     email,
                     first_name,
                     last_name,
                     city,
                     country,
                     gender,
                     password
                 )
                 VALUES (
                     'email1',
                     'first_name',
                     'last_name',
                     'city',
                     'country',
                     'male',
                     '1234567890'
                 );

INSERT INTO User (
                     email,
                     first_name,
                     last_name,
                     city,
                     country,
                     gender,
                     password
                 )
                 VALUES (
                     'talha@abc.com',
                     'talha',
                     'talha',
                     'Sweden',
                     'linkoping',
                     'male',
                     '1234567890'
                 );

INSERT INTO User (
                     email,
                     first_name,
                     last_name,
                     city,
                     country,
                     gender,
                     password
                 )
                 VALUES (
                     'talha1@abc.com',
                     'talha',
                     'talha',
                     'Sweden',
                     'linkoping',
                     'male',
                     '1234567890'
                 );

INSERT INTO User (
                     email,
                     first_name,
                     last_name,
                     city,
                     country,
                     gender,
                     password
                 )
                 VALUES (
                     'talha2@abc.com',
                     'talha',
                     'talha',
                     'Sweden',
                     'linkoping',
                     'male',
                     '1234567890'
                 );


-- Table: UserSession
CREATE TABLE UserSession (
    id         INTEGER       PRIMARY KEY AUTOINCREMENT,
    token      VARCHAR (255) NOT NULL,
    status     VARCHAR (10)  CHECK (status IN ('logedIn', 'logedOut') ) 
                             NOT NULL,
    user_email VARCHAR (255) REFERENCES User (email) 
);

INSERT INTO UserSession (
                            id,
                            token,
                            status,
                            user_email
                        )
                        VALUES (
                            1,
                            '12345',
                            'logedOut',
                            'talha@abc.com'
                        );

INSERT INTO UserSession (
                            id,
                            token,
                            status,
                            user_email
                        )
                        VALUES (
                            2,
                            '123456',
                            'logedOut',
                            'talha1@abc.com'
                        );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
