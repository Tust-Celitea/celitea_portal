import os
from flask import Flask
from app import create_app, db
from app.models import User, Follow, Role, Permission, Post, Comment ,Group
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


def wsgi_create_app():
  app = create_app(os.getenv('FLASK_CONFIG') or 'default')
  return app

application = wsgi_create_app()

if __name__ == '__main__':
    application.run()
