from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = []
    if request.method == 'GET':
        #messages = []
        for message in Message.query.all():
            message_dict = {
                "id": message.id,
                "body": message.body,
                "username": message.username,
                "created_at": message.created_at,
                "updated_at": message.updated_at
            }
            messages.append(message_dict)

            response = make_response(jsonify(messages), 200)

        return response
    
    elif request.method == 'POST':
        message = request.get_json()
        new_message = Message(
            body=message["body"],
            username=message["username"]
        )
        db.session.add(new_message)
        db.session.commit()

        message_serialized = new_message.to_dict()

    response = make_response(jsonify(message_serialized), 201)
    return response
        

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == 'PATCH':
        msg = request.get_json()
        message.body = msg["body"]
        db.session.add(message)
        db.session.commit()

        message_serialized = message.to_dict()
        response = make_response(message_serialized, 200)

        return response
    else:
        db.session.delete(message)
        db.session.commit()
        return ''
    

if __name__ == '__main__':
    app.run(port=5555)