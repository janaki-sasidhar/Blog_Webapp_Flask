from flask import Flask, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView
from flask_blogg.config import Config
from flask_misaka import Misaka


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not current_user.is_anonymous:
            if current_user.email == 'janakisasidhar1@gmail.com':
                return True
            else:
                return False
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        flash('You dont have rights to access this page', 'danger')
        return redirect(url_for('main.index'))


app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
md = Misaka()
admin = Admin(index_view=MyAdminIndexView(), template_mode='bootstrap3')
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "danger"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)
    md.init_app(app)
    from flask_blogg.users.routes import users
    from flask_blogg.posts.routes import posts
    from flask_blogg.main.routes import main
    from flask_blogg.main.routes import errors
    from flask_blogg.paste.routes import paste

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(paste)
    return app
