import os
import pathlib

import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI", f"sqlite:///{basedir / 'people.db'}")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
