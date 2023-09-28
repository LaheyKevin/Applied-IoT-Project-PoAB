import os

basedir = os.path.abspath(
    os.path.dirname(__file__)
)  # top-level locatie van onze toepassing


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "mijn-secret-key-niet-veilig"

