from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

CORS(app)

class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(50), unique=True, nullable=False)

@app.route("/")
def hello_World():
  return {"Hello": "cross-origin-world!"}

@app.route("/home")
def home():
    users = User.query.all()
    users_list = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(users_list)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)