from flask import Flask  # alleen wat we nodig hebben!

from config import Config


app = Flask(__name__)  # naam vd package
app.config.from_object(Config)
from app import routes  # beneden om circular dependency probleem te omzeilen
