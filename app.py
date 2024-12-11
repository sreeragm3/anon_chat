from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, send
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
socketio = SocketIO(app)

# Store connected users with their usernames
users = {}

@app.route('/')
def index():
    if 'username' not in session:
        session['username'] = f'User-{uuid.uuid4().hex[:6]}'  # Generate a temporary unique username
    return render_template('index.html', username=session['username'])

@socketio.on('connect')
def handle_connect():
    username = session.get('username', f'User-{uuid.uuid4().hex[:6]}')
    users[request.sid] = username
    print(f'{username} connected.')

@socketio.on('disconnect')
def handle_disconnect():
    username = users.pop(request.sid, None)
    print(f'{username} disconnected.')

@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, 'Unknown')
    formatted_message = f'{username}: {msg}'
    print(formatted_message)
    send(formatted_message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
