from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pagedown import PageDown
import os
import click

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
pagedown = PageDown()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "super-secret-key")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "mysql://journaluser:journalpass@db:3306/teacher_journal")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    pagedown.init_app(app)

    @app.cli.command("create-admin")
    @click.argument("username")
    @click.argument("password")
    def create_admin(username, password):
        if User.query.filter_by(username=username).first():
            click.echo("Пользователь с таким именем уже существует.")
            return
        user = User(username=username, role='admin')
        user.set_password(password)  # метод должен быть в вашей модели User
        db.session.add(user)
        db.session.commit()
        click.echo(f"Администратор {username} успешно создан!")

    @app.cli.command("create-user")
    @click.argument("username")
    @click.argument("password")
    @click.argument("role")  # 'teacher' или 'student' или 'admin'
    def create_user(username, password, role):
        if role not in ['admin', 'teacher', 'student']:
            click.echo("Роль должна быть одной из ['admin', 'teacher', 'student']")
            return
        if User.query.filter_by(username=username).first():
            click.echo("Пользователь с таким именем уже существует.")
            return
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Пользователь {username} с ролью {role} успешно создан!")

    from .routes import bp
    app.register_blueprint(bp)

    return app
