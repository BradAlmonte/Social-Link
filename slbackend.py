from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    interests = db.Column(db.Text, nullable=False)  # Comma-separated interests

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        password_hash=hashed_password,
        age=data['age'],
        location=data['location'],
        interests=','.join(data['interests'])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

@app.route('/api/suggestions/<username>', methods=['GET'])
def suggestions(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found!"}), 404
    
    user_interests = set(user.interests.split(','))
    suggestions = User.query.filter(
        User.id != user.id,
        abs(User.age - user.age) <= 5,
        User.location == user.location
    ).all()

    results = []
    for s in suggestions:
        shared_interests = user_interests.intersection(set(s.interests.split(',')))
        if shared_interests:
            results.append({"username": s.username, "shared_interests": list(shared_interests)})
    
    return jsonify({"suggestions": results})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
