from flask import *
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DATA.db'
app.config['SECRET_KEY'] = 'CODINARMS@'
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(400), nullable=False)

    def __repr__(self):
        return self.username


class BlogSchema(ma.Schema):
    class Meta:
        fields = ['username', 'password', 'id']


blog_schema = BlogSchema()
blog_schemas = BlogSchema(many=True)


@app.route("/", methods=['GET'])
def home_view():
    blogs = Blog.query.all()
    return blog_schemas.jsonify(blogs)


@app.route("/get/<int:pk>", methods=['GET'])
def get_blog_view(pk):
    blog = Blog.query.get(pk)
    return blog_schema.jsonify(blog)


@app.route("/update/<int:pk>", methods=['PUT'])
def update_view(pk):
    blog = Blog.query.get(pk)
    blog.username = request.json['username']
    blog.password = request.json['password']
    blog.commit()
    return blog_schema.jsonify(blog)


@app.route("/delete/<int:pk>", methods=['GET', 'DELETE'])
def delete_view(pk):
    try:
        blog = Blog.query.get(pk)
        db.session.delete(blog)
        db.session.commit()
        return blog_schema.jsonify(blog)
    except:
        return redirect(url_for('home_view'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
