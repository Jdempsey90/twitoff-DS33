from flask_sqlalchemy import SQLAlchemy


# create db
DB = SQLAlchemy()


# create tables
class User(DB.Model):
    # each dm col will be a class attribute

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

    newest_tweet_id = DB.Column(
        DB.BigInteger
        )


class Tweet(DB.Model):

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
