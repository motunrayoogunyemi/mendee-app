from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from flask_migrate import Migrate

import config       #(this is the config in the root) this is how to import things that are on the same level

app = Flask(__name__,instance_relative_config=True)                 #config in instance folder
csrf = CSRFProtect(app)
app.config.from_pyfile('config.py')                                 #config in instance folder
app.config.from_object(config.ProductionConfig)                     #config in the root

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#load the routes
from mendeeapp.routes import user_routes,admin_routes
from mendeeapp import mymodels