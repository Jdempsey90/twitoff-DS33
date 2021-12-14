from flask import Flask, render_template
from .models import DB, User, Tweet


# app factory
def create_app():

    # initialize Flask app
    app = Flask(__name__)

    # configuration stuff
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'

    # connect app to DB
    DB.init_app(app)

    # make root route
    @app.route('/')
    def root():
        return render_template('base.html')

    @app.route('/test')
    def test():
        # create user in DB
        DB.drop_all()
        DB.create_all()

        # create user object
        ryan = User(id=1, username='ryanallred')
        julian = User(id=2, username='Jullian')

        # add object to DB
        DB.session.add(ryan)
        DB.session.add(julian)

        # fake tweets
        tweet1 = Tweet(
            id=1,
            text="this is some tweet text",
            user=ryan
            )
        tweet2 = Tweet(
            id=2,
            text="this is some different tweet text",
            user=julian
            )
        tweet3 = Tweet(
            id=3,
            text="a third tweet",
            user=ryan
            )
        tweet4 = Tweet(
            id=4,
            text="a fourth tweet",
            user=julian
            )
        tweet5 = Tweet(
            id=5,
            text="number 5",
            user=ryan
            )
        tweet6 = Tweet(
            id=6,
            text="Number 6!",
            user=julian
            )

        DB.session.add(tweet1)
        DB.session.add(tweet2)
        DB.session.add(tweet3)
        DB.session.add(tweet4)
        DB.session.add(tweet5)
        DB.session.add(tweet6)

        # commit changes
        DB.session.commit()

        # query for users
        users = User.query.all()

        return render_template('base.html', users=users)

    return app
