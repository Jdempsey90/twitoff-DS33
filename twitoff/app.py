'''Flask Factory'''

from os import getenv
from flask import Flask, render_template, request
from .predict import predict_user
from .models import DB, User
from .twitter import add_or_update_user


# app factory
def create_app():
    '''Flask Factory

    Returns:
        Flask App
    '''
    # initialize Flask app
    app = Flask(__name__)

    # configuration stuff
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABASE_URI')

    # connect app to DB
    DB.init_app(app)

    # define root route
    @app.route('/')
    def root():
        '''Home route

        Returns:
            returns templated html
        '''
        return render_template(
            'base.html',
            title='Home',
            users=User.query.all()
            )

    # define update route
    @app.route('/update')
    def update():
        '''Update route

        Returns:
            a fixed string
        '''
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            add_or_update_user(username)
        return '''Database has been UPDATED!'''

    # define reset route
    @app.route('/reset')
    def reset():
        '''Reset route

        Returns:
            returns templated html
        '''
        # create user in DB
        DB.drop_all()
        DB.create_all()

        return render_template("base.html", title="Reset Database")

    @app.route('/user', methods=["POST"])
    @app.route('/user/<name>', methods=["GET"])
    def user(name=None, message=''):

        # we either take name that was passed in or we pull it
        # from our request.values which would be accessed through the
        # user submission
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f"User {name} Successfully added!"

            tweets = User.query.filter(User.username == name).one().tweets

        except Exception as e:
            message = "Error adding {}: {}".format(name, e)

            tweets = []

        return render_template(
            "user.html",
            title=name,
            tweets=tweets,
            message=message
            )

    @app.route('/compare', methods=["POST"])
    def compare():
        user0, user1 = sorted(
            [request.values['user0'], request.values["user1"]]
            )

        if request.values["tweet_text"]:
            if user0 == user1:
                message = "Cannot compare users to themselves!"

            else:
                # prediction returns a 0 or 1
                prediction = predict_user(
                    user0, user1, request.values["tweet_text"])

                message = "\
                    '{}' is more likely to be said by {} than {}!\
                    ".format(

                    request.values["tweet_text"],
                    user1 if prediction else user0,
                    user0 if prediction else user1
                )
        else:
            message = "You must include tweet text before comparing users."

        return render_template(
                'prediction.html',
                title="Prediction",
                message=message
                )

    return app
