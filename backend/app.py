from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from database.db import initialize_db
from flask_restful import Api
from resources.errors import errors

app = Flask(__name__)
app.config["JWT_TOKEN_LOCATION"] = ["cookies", "query_string", "json"]
app.config["JWT_HEADER_NAME"] = "TestHeader"
app.config["JWT_HEADER_TYPE"] = "TestType"
app.config["JWT_JSON_KEY"] = "TestKey"
app.config["JWT_REFRESH_JSON_KEY"] = "TestRefreshKey"

app.config["JWT_DECODE_ISSUER"] = "TestDecodeIssuer"
app.config["JWT_ENCODE_ISSUER"] = "TestEncodeIssuer"

app.config["JWT_QUERY_STRING_NAME"] = "banana"
app.config["JWT_QUERY_STRING_VALUE_PREFIX"] = "kiwi"

app.config["JWT_ACCESS_COOKIE_NAME"] = "new_access_cookie"
app.config["JWT_REFRESH_COOKIE_NAME"] = "new_refresh_cookie"
app.config["JWT_ACCESS_COOKIE_PATH"] = "/access/path"
app.config["JWT_REFRESH_COOKIE_PATH"] = "/refresh/path"
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_COOKIE_DOMAIN"] = ".example.com"
app.config["JWT_SESSION_COOKIE"] = False
app.config["JWT_COOKIE_SAMESITE"] = "Strict"

app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_CSRF_METHODS"] = ["GET"]
app.config["JWT_CSRF_IN_COOKIES"] = False
app.config["JWT_ACCESS_CSRF_COOKIE_NAME"] = "access_csrf_cookie"
app.config["JWT_REFRESH_CSRF_COOKIE_NAME"] = "refresh_csrf_cookie"
app.config["JWT_ACCESS_CSRF_COOKIE_PATH"] = "/csrf/access/path"
app.config["JWT_REFRESH_CSRF_COOKIE_PATH"] = "/csrf/refresh/path"
app.config["JWT_ACCESS_CSRF_HEADER_NAME"] = "X-ACCESS-CSRF"
app.config["JWT_REFRESH_CSRF_HEADER_NAME"] = "X-REFRESH-CSRF"

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 24*60
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 24*60
app.config["JWT_ALGORITHM"] = "HS512"
app.config["JWT_DECODE_ALGORITHMS"] = ["HS512", "HS256"]

app.config["JWT_IDENTITY_CLAIM"] = "foo"

app.config["JWT_ERROR_MESSAGE_KEY"] = "message"

app.config["JWT_SECRET_KEY"] = "inisangatrahasiasekali"
mail = Mail(app)

# imports requiring app and mail
from resources.routes import initialize_routes

api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_db(app)
initialize_routes(api)
