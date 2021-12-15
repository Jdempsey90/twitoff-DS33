'''Flask Factory'''

from flask import Flask, render_template
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
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'

    # connect app to DB
    DB.init_app(app)

    # define root route
    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', users=users)

    # define update route
    @app.route('/update')
    def update():
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            add_or_update_user(username)
        return '''Database has been UPDATED!\n
        <a href='/'>HOME  </a>\
        <a href='/reset'> RESET </a>\
        <a href='/populate'> POPULATE</a>'''

    # define populate route
    @app.route('/populate')
    def populate():
        add_or_update_user('ryanallred')
        add_or_update_user('NASA')

        return '''USERS CREATED\n
        <a href='/'>HOME  </a>\
        <a href='/reset'> RESET </a>\
        <a href='/populate'> POPULATE</a>'''

    # define reset route
    @app.route('/reset')
    def reset():
        # create user in DB
        DB.drop_all()
        DB.create_all()

        return '''Database has been RESET!\n
        <a href='/'>HOME  </a>\
        <a href='/reset'> RESET </a>\
        <a href='/populate'> POPULATE</a>'''

    return app
