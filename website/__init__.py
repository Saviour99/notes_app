from flask import Flask

def notes_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Dela.dev"

    return app