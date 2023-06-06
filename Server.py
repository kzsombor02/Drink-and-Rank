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
    friend_ids = [friend_id[0] for friend_id in friend_ids] #  gets the first element of each tuple in the list
    return db_session.query(User).filter(User.id.in_(friend_ids)).all() #  gets all the friends of the user

def get_rank(user):
    return db_session.query(User).filter(User.points >= user.points).count() #  gets the number of users with more points than the user

def handle_client(client_socket):
    try:
        data = client_socket.recv(1024) #  receives the username from the client
        username = data.decode().strip() #  decodes the username

        user = db_session.query(User).filter(User.name == username).first() #  gets the user from the database
        if user: #  if the user exists
            friends = get_friends(user) #  gets the friends of the user

            friend_list = [] #  creates a list of friends
            for friend in friends: #  for each friend
                friend_list.append({'name': friend.name}) #  adds the friend's name to the list

            rank = get_rank(user) #  gets the rank of the user

            response = {
                'success': True,
                'message': 'Username exists.', #  sends the user's data to the client
                'data': {
                    'name': user.name,
                    'age': user.age,
                    'points': user.points,
                    'rank': rank,
                    'friends': friend_list
                }
            }
        else:
            response = {'success': False, 'message': 'Username does not exist.'} #  sends an error message to the client

        response_json = json.dumps(response).encode() #  encodes the response
        client_socket.sendall(response_json) #  sends the response to the client

        if user: #  if the user exists
            data = client_socket.recv(1024) #  receives the friend's name from the client
            friend_name = data.decode().strip() #  decodes the friend's name

            friend = db_session.query(User).filter(User.name == friend_name).first() #  gets the friend from the database
            if friend:
                friend_data = { #  sends the friend's data to the client
                    'name': friend.name,
                    'age': friend.age,
                    'points': friend.points,
                    'rank': get_rank(friend)
                }
                response = {'success': True, 'message': 'Friend data retrieved.', 'data': friend_data} #  sends the friend's data to the client
            else:
                response = {'success': False, 'message': 'Friend does not exist.'} #  sends an error message to the client

            response_json = json.dumps(response).encode() #  encodes the response
            client_socket.sendall(response_json) #  sends the response to the client

    except Exception as e: #  if an error occurs
        print(f"Error handling client: {e}")  #  prints the error
    finally:
        client_socket.close() #  closes the client socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #  creates a socket
server_socket.bind((HOST, PORT)) #  binds the socket to the host and port
server_socket.listen(1) #  listens for connections

print(f"Server listening on {HOST}\nPort: {PORT}") #  prints the host and port

while True:
    client_socket, address = server_socket.accept() #  accepts a connection
    print(f"Accepted connection from {address[0]}: {address[1]}") #  prints the address of the client
    handle_client(client_socket) #  handles the client
