import socket
import json
from sqlalchemy.orm import sessionmaker
from Database_test import User, Friendships, engine

HOST = '127.0.0.1'
PORT = 9000

# Establish database connection
Session = sessionmaker(bind=engine)
db_session = Session()

def get_friends(user):
    friend_ids = db_session.query(Friendships.friend_id).filter_by(user_id=user.id, status="accepted").all() #  gets all the friend ids of the user
    friend_ids = [friend_id[0] for friend_id in friend_ids]
    return db_session.query(User).filter(User.id.in_(friend_ids)).all()

def get_rank(user):
    return db_session.query(User).filter(User.points >= user.points).count()

def handle_client(client_socket):
    try:
        data = client_socket.recv(1024)
        username = data.decode().strip()

        user = db_session.query(User).filter(User.name == username).first()
        if user:
            friends = get_friends(user)

            friend_list = []
            for friend in friends:
                friend_list.append({'name': friend.name})

            rank = get_rank(user)

            response = {
                'success': True,
                'message': 'Username exists.',
                'data': {
                    'name': user.name,
                    'age': user.age,
                    'points': user.points,
                    'rank': rank,
                    'friends': friend_list
                }
            }
        else:
            response = {'success': False, 'message': 'Username does not exist.'}

        response_json = json.dumps(response).encode()
        client_socket.sendall(response_json)

        if user:
            data = client_socket.recv(1024)
            friend_name = data.decode().strip()

            friend = db_session.query(User).filter(User.name == friend_name).first()
            if friend:
                friend_data = {
                    'name': friend.name,
                    'age': friend.age,
                    'points': friend.points,
                    'rank': get_rank(friend)
                }
                response = {'success': True, 'message': 'Friend data retrieved.', 'data': friend_data}
            else:
                response = {'success': False, 'message': 'Friend does not exist.'}

            response_json = json.dumps(response).encode()
            client_socket.sendall(response_json)

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on {HOST}\nPort: {PORT}")

while True:
    client_socket, address = server_socket.accept()
    print(f"Accepted connection from {address[0]}: {address[1]}")
    handle_client(client_socket)
