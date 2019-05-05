from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from evocloud.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'views.login'

# run scheduler
import evocloud.jobs

from evocloud.views import routes
app.register_blueprint(routes)
