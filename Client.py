import socket
import json

HOST = '127.0.0.1'
PORT = 9000

def send_username(username):
    try: # try to execute the code inside the try block
        # Connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        # Send the username to the server
        client_socket.sendall(username.encode()) # send the username to the server

        # Receive the response from the server
        data = client_socket.recv(1024) # receive the data from the server
        response = json.loads(data.decode()) # decode the data and convert it to a dictionary

        # Process the response
        if response['success']: # if the response is successful
            print(response['message'])
            user_data = response['data']
            print("User Data:")
            print(f"Name: {user_data['name']}")
            print(f"Age: {user_data['age']}")
            print(f"Points: {user_data['points']}\n")

            if 'friends' in user_data:
                friend_list = user_data['friends']
                print(f"{username}'s Friend List:")
                for friend in friend_list:
                    print(f"Name: {friend['name']}")

            friend_name = input("View friend's profile: ")

            # Send friend name to the server for retrieval
            client_socket.sendall(friend_name.encode())

            # Receive the response from the server
            data = client_socket.recv(1024)
            response = json.loads(data.decode())

            # Process the response
            if response['success']:
                friend_data = response['data']
                print("\nFriend Data:")
                print(f"Name: {friend_data['name']}")
                print(f"Age: {friend_data['age']}")
                print(f"Points: {friend_data['points']}")

            compare_points = input("Compare points with friend? (yes/no): ")

            if compare_points.lower() == "yes":
                # Compare points and rankings
                if user_data['points'] > friend_data['points']:
                    print(f"{username} has more points than {friend_data['name']}")
                elif user_data['points'] < friend_data['points']:
                    print(f"{friend_data['name']} has more points than {username}")
                else:
                    print(f"{username} and {friend_data['name']} have the same number of points")

                if user_data['points'] > friend_data['points'] and user_data['rank'] > friend_data['rank']:
                    print(f"{username} is ranked higher than {friend_data['name']}")
                elif user_data['points'] < friend_data['points'] and user_data['rank'] < friend_data['rank']:
                    print(f"{friend_data['name']} is ranked higher than {username}")
                elif user_data['rank'] == friend_data['rank']:
                    print(f"{username} and {friend_data['name']} have the same rank")


            else:
                print(response['message'])

        else:
            print(response['message'])
    except Exception as e: # if there is an error in the try block, the code inside the except block will be executed
        print(f"Error connecting to server: {e}") # print the error
    finally:
        client_socket.close() # close the client socket

# Prompt for username
username = input("Enter your username: ")

# Send the username to the server for validation
send_username(username) # send the username to the server
