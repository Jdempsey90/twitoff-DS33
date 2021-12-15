'''sqlalchemy models'''

from flask_sqlalchemy import SQLAlchemy


# create db
DB = SQLAlchemy()


# create tables
class User(DB.Model):
    '''Defines the User table in the sqlite
    database
    '''

    # create id attribute
    id = DB.Column(
        DB.BigInteger,
        primary_key=True,
        nullable=False
        )

    # create username attribute
    username = DB.Column(
        DB.String,
        nullable=False
        )

    # create newest_tweet_id attribute
    newest_tweet_id = DB.Column(
        DB.BigInteger
        )


class Tweet(DB.Model):
    '''Defines the Tweet table in the sqlite
    database
    '''
    id = DB.Column(
        DB.BigInteger,
        primary_key=True,
        nullable=False
        )

    text = DB.Column(
        DB.Unicode(300),
        nullable=False
        )

    vect = DB.Column(
        DB.PickleType,
        nullable=False
    )

    user_id = DB.Column(
        DB.BigInteger,
        DB.ForeignKey('user.id'),
        nullable=False
        )

    # automatically add new id to both the tweet and the user
    user = DB.relationship(
        'User',
        backref=DB.backref('tweets'),
        lazy=True
        )
