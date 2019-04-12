import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

#DATABASE_URI="postgres://reinhard:password@localhost:5432/apidatabase"
#https://git.heroku.com/reinhard-api.git
#https://reinhard-api.herokuapp.com/

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

app.config.from_object(os.getenv('APP_SETTINGS'))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# import models
from models import *

@app.route("/")
def hello():
    return ("Hello, World!")

@app.route("/add")
def add_book():
    name=request.args.get("name")
    author=request.args.get("author")
    published=request.args.get("published")
    try :
        book = Book(
            name=name,
            author=author,
            published=published
        )
        db.session.add(book)
        db.session.commit()
        return "Book added. book id ={}".format(book.id)
    except Exception as e:
        return(str(e))

@app.route("/getall")
def get_all():
    try:
        books = Book.query.all()
        return jsonify([e.serialize() for e in books])
    except Exception as e:
        return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book = Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
        return (str(e))

if __name__ == "__main__":
    app.run(debug=True)
