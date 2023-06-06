import json
from Database_test import User, Friendships, Drink, Rating, session


class Database:
    def create_user(self, name, age):
        user = User(name=name, age=age, points=0) # create a user object
        session.add(user) # add the user object to the session
        session.commit() # commit the session to the database

    def update_user_points(self, name, points):
        user = self.get_user_by_name(name) # get the user object from the database
        user.points += points # update the user's points
        session.commit() # commit the session to the database

    def get_user_by_name(self, name):
        return session.query(User).filter_by(name=name).first() # query the database for the user object

    def get_all_users(self):
        return session.query(User).all() # query the database for all user objects

    def delete_user(self, name):
        user = self.get_user_by_name(name) # get the user object from the database
        if user: # if the user exists
            session.delete(user) # delete the user object from the database
            session.commit()

    def add_friend(self, user, friend):
        friendship1 = Friendships(user_id=user.id, friend_id=friend.id, status="pending") # creates a friendship object
        friendship2 = Friendships(user_id=friend.id, friend_id=user.id, status="pending")
        session.add_all([friendship1, friendship2]) # add the friendship objects to the session
        session.commit() # commit the session to the database

    def view_friend_requests(self, user):
        friend_ids = session.query(Friendships.friend_id).filter_by(user_id=user.id, status="pending").all() # query the database for the friend ids, if status is pending, executes the query and retrieves all results
        friend_ids = [friend_id[0] for friend_id in friend_ids] #iterates over each element and retrieves the first item from each tuple
        return session.query(User).filter(User.id.in_(friend_ids)).all() #if the user id is in the list of friend ids, return all the users


    def accept_friend_request(self, user, friend):
        friendship1 = session.query(Friendships).filter_by(user_id=user.id, friend_id=friend.id).first() # query the database for the friendship object
        friendship2 = session.query(Friendships).filter_by(user_id=friend.id, friend_id=user.id).first()
        friendship1.status = "accepted" # update the friendship object's status
        friendship2.status = "accepted"
        session.commit() # commit the session to the database

    def get_friends(self, user):
        friend_ids = session.query(Friendships.friend_id).filter_by(user_id=user.id, status="accepted").all() # query the database for the friend ids, if status is accpeted, executes the query and retrieves all results
        friend_ids = [friend_id[0] for friend_id in friend_ids] #iterates over each element and retrieves the first item from each tuple
        return session.query(User).filter(User.id.in_(friend_ids)).all() #if the user id is in the list of friend ids, return all the users

    def display_leaderboard(self):
        users = session.query(User).order_by(User.points.desc()).all() # query the database for all user objects, order by points in descending order
        print("Leaderboard:")
        for index, user in enumerate(users, start=1): #Returning the user and its index in the list
            print(f"{index}. {user.name} - Points: {user.points}") # print the user's name and points and its index in the list


class DrinkAndRank:
    def __init__(self):
        self.beverages = {} # dictionary to store the beverages
        self.user = None # variable to store the user object

    def load_beverages(self, filename):
        with open(filename) as f:
            self.beverages = json.load(f)

    def display_menu(self):
        print("Welcome to Drink and Rank!")
        print("Here is our menu: ")
        for category in self.beverages:
            print(f"{category}:") # prints the categories

    def select_category(self):
        while True: # loop until a valid category is selected
            category = input("Please select a category: ")
            if category in self.beverages: # if the category exists
                self.process_category(category) # process the category
                break # exit the loop
            else: # if the category does not exist
                print("Invalid category. Please try again.") # print error message

    def select_beverage(self, category):
        while True: # loop until a valid beverage is selected
            choose = input("Please choose a drink: ")
            if choose in self.beverages[category]: # if the beverage exists
                beverage = self.beverages[category][choose] # get the beverage object
                strength = beverage["strength"] # get the beverage's strength
                print(f"You have chosen {choose}. Strength: {strength}") # print the beverage's name and strength
                self.add_points(self.user, strength) # add points to the user
                break
            else:
                print("Invalid drink. Please try again.")

    def add_points(self, user, strength):
        points = strength # points are equal to the beverage's strength
        user.points += points # add points to the user
        session.commit() # commit the session to the database
        print(f"You have earned {points} points!") # print the number of points earned

    def process_category(self, category):
        print(f"Selected category: {category}") # print the selected category
        print("Here are the beverages in this category: ") # print the beverages in the category
        for beverage in self.beverages[category]: # iterate over the beverages in the category
            print(beverage) # print the beverage's name
        self.select_beverage(category) # select a beverage

    def run(self):
        filename = "beverages.json"
        self.load_beverages(filename) # load the beverages from the file
        self.display_menu() # display the menu
        self.select_category() # select a category


class UserManagement:
    def create_profile(self):
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))
        db.create_user(name, age) # create a user object
        print(f"Profile created for {name}.")

    def update_profile(self, user):
        name = input("Enter your new name (leave blank to keep the current name): ")
        if name.strip() != "": # if the name is not blank
            user.name = name # update the user's name
        session.commit() # commit the session to the database
        print(f"Profile updated for {user.name}.") # print the user's name

    def add_friend(self, user):
        friend_name = input("Enter your friend's name: ")
        friend = db.get_user_by_name(friend_name) # query the database for the friend
        if friend: # if the friend exists
            db.add_friend(user, friend) # add the friend
            print(f"Friend request sent to {friend.name}.")
        else:
            print("Friend not found.")

    def view_friend_requests(self, user):
        friend_requests = db.view_friend_requests(user) # query the database for the friend requests
        if friend_requests: # if there are friend requests
            print("Friend Requests:") # print the friend requests
            for friend_request in friend_requests: # iterate over the friend requests
                print(friend_request.name) # print the friend's name
        else:
            print("You have no friend requests.")

    def accept_friend_request(self, user):
        friend_name = input("Enter your friend's name: ") # get the friends name
        friend = db.get_user_by_name(friend_name) # query the database for the friend
        if friend: # if the friend exists
            db.accept_friend_request(user, friend) # accept the friend request
            print(f"You are now friends with {friend.name}.")
        else:
            print("Friend not found.")

    def view_friend_list(self, user): # query the database for the user's friends
        friends = db.get_friends(user) # get the user's friends
        if friends: # if the user has friends
            print("Friend List:")
            for friend in friends:
                print(friend.name)
        else:
            print("You have no friends yet.")

    def display_stats(self, user): # display the user's stats
        print(f"Name: {user.name}")
        print(f"Age: {user.age}")
        print(f"Points: {user.points}")


db = Database()
app = DrinkAndRank()
user_manager = UserManagement()

while True:
    print("==============")
    print("1. Create Profile")
    print("2. Update Profile")
    print("3. Add Friend")
    print("4. View Friend Request")
    print("5. Accept Friend Request")
    print("6. View Friend List")
    print("7. Display Stats")
    print("8. Display Leaderboard")
    print("9. Start Ordering")
    print("10. Play in Tkinter")
    choice = input("Enter your choice: ")

    if choice == "1":
        user_manager.create_profile() # create a profile
    elif choice == "2":
        name = input("Enter your name: ")
        user = db.get_user_by_name(name) # query the database for the user
        if user:
            user_manager.update_profile(user) # update the users profile
        else:
            print("User not found.")
    elif choice == "3":
        name = input("Enter your name: ")
        user = db.get_user_by_name(name) # query the database for the user
        if user:
            user_manager.add_friend(user) # add a friend
        else:
            print("User not found.")
    elif choice == "4":
        name = input("Enter your name: ")
        user = db.get_user_by_name(name) # query the database for the user
        if user:
            user_manager.view_friend_requests(user) # view friend requests
        else:
            print("User not found.")
    elif choice == "5":
        name = input("Enter your name: ")
        user = db.get_user_by_name(name) # query the database for the user
        if user:
            user_manager.accept_friend_request(user) # accept a friend request
        else:
            print("User not found.")
    elif choice == "6":
        name = input("Enter your name: ")
        user = db.get_user_by_name(name)
        if user:
            user_manager.view_friend_list(user) # view the user's friend list
        else:
            print("User not found.")
    elif choice == "7":
        name = input("Enter your name: ")
        user = db.get_user_by_name(name)
        if user:
            user_manager.display_stats(user) # display the user's stats
        else:
            print("User not found.")
    elif choice == "8":
        db.display_leaderboard() # display the leaderboard
    elif choice == "9":
        name = input("Enter your name: ")
        user = db.get_user_by_name(name)
        if user:
            app.user = user
            app.run()
        else:
            print("User not found.")
    elif choice == "10":
        break
    else:
        print("Invalid choice. Please try again.")