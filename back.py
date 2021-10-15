from flask import (render_template, Flask, json, jsonify, redirect, request, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posters/posters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app, resources={r'/*': {'orgins': '*'}})
poster = SQLAlchemy(app)
ma = Marshmallow(app)

class PosterDep(poster.Model):
    id = poster.Column(poster.Integer, primary_key=True)
    name = poster.Column(poster.String(30), nullable=False)
    price = poster.Column(poster.String(14), nullable=False)
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return "user" + str(self.id)

class PostSchema(ma.Schema):
    class Meta:
        fields = ('id','name','price')
user_schema = PostSchema()
users_schema = PostSchema(many=True)


@app.route('/posts/get', methods=['GET'])
def posts_route():
    users = PosterDep.query.all()
    users_results = users_schema.dump(users)
    return jsonify(users_results)


@app.route('/posts/update/<int:id>', methods=['PUT'])
def update_user(id):
    user = PosterDep.query.get(id)
    name = request.json['name']
    price = request.json['price']
    if name == "" and price == "":
        return user_schema.jsonify(user)
    else:
        user.name = name
        user.price = price
        poster.session.commit()
    return user_schema.jsonify(user)


@app.route('/posts/add', methods=['POST'])
def add_post():
    all_users = PosterDep.query.all()
    name = request.json['name']
    price = request.json['price']
    user_post = PosterDep(name=name, price=price)
    poster.session.add(user_post)
    poster.session.commit()
    return user_schema.jsonify(user_post)
 
@app.route('/posts/delete/<int:id>', methods=['DELETE'])
def delete_route(id):
    user = PosterDep.query.get(id)
    users = PosterDep.query.all()
    poster.session.delete(user)
    poster.session.commit()
    return user_schema.jsonify(user)

if '__main__' == __name__:
    app.run(port=2020, debug=True)