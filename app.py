from flask import Blueprint
import os
from config import app, db
from post.index import posts
from sorvetes.sorvete_routes import sorvete_blueprint


app.register_blueprint(posts)
app.register_blueprint(sorvete_blueprint)

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port = app.config['PORT'], debug = app.config['DEBUG'])