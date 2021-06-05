from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from logging.handlers import  SMTPHandler, RotatingFileHandler

from config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    if not app.debug and not app.testing:
        if app.config["MAIL_SERVER"]:
            auth = None
            if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
                auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            secure = None
            if app.config["MAIL_USE_TLS"]:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
                fromaddr=f"no-reply@{app.config['MAIL_SERVER']}",
                toaddrs=app.config["ADMINS"],
                subject="Microblog Failure",
                credentials=auth,
                secure=secure,
                # timeout=...
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if app.config["LOG_TO_STDOUT"]:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)

        else:    
            if not os.path.exists("logs"):
                os.mkdir("logs")                
            file_handler = RotatingFileHandler("logs/playground.log",
                                                maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s "
                "[in %(pathname)s:%(lineno)d]"))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Playground startup")

    return app


from application import models
