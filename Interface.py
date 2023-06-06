import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from Database_test import User, Friendships, Drink, Rating, session
from DrinkAndRank import Database as DB
import socket
import threading




class DrinkAndRankGUI:
    def __init__(self, master): # master is the root window
        self.master = master
        self.master.title("Drink&Rank")
        self.master.geometry("400x950")
        self.load_beverages("beverages.json")

        primary_color = "#3EB489"  # Light green color
        secondary_color = "#1B262C"
        button_color = "#E8E8E8"

        # Set the Drink&Rank title label
        title_image = tk.PhotoImage(file="Drink&Rank.png")
        self.title_label = tk.Label(master, image=title_image)
        self.title_label.image = title_image
        self.title_label.pack(pady=10)



        # Create the options frame
        self.options_frame = tk.Frame(master, bg=primary_color) # Create a frame to hold the buttons
        self.options_frame.pack(pady=20) # Add  padding around the frame

        button_style = {"font": ("Arial", 14), "bg": button_color, "fg": secondary_color, "width": 20, "height": 1}



        # Create the function buttons
        self.function_buttons = []
        functions = [
            ("Create Profile", self.create_profile),
            ("Update Profile", self.update_profile),
            ("Add Friend", self.add_friend),
            ("View Friend Requests", self.view_friend_requests),
            ("Accept Friend Request", self.accept_friend_request),
            ("View Friend List", self.view_friend_list),
            ("Display Stats", self.display_stats),
            ("Display Leaderboard", self.display_leaderboard),
            ("Start Ordering", self.start_ordering),
            ("Delete Profile", self.delete_user),
            ("Exit", self.exit_app)
        ]
        for button_text, button_command in functions: # Loop through the list of functions
            button = tk.Button(self.options_frame, text=button_text, **button_style, command=button_command) # Create a button
            button.pack(pady=10)
            self.function_buttons.append(button)  # Add the button to the list of function buttons
        self.db = DB() # Create a database object



    def create_title_label(self, text):
        self.title_label = tk.Label(self.master, text=text, font=("Arial", 16, "bold")) # Create the title label
        self.title_label.pack(pady=10)

    def create_options_frame(self):
        self.options_frame = tk.Frame(self.master) # Create a frame to hold the buttons
        self.options_frame.pack(pady=20)

    def create_function_buttons(self, functions):
        self.function_buttons = []
        for function in functions:
            button = tk.Button(self.options_frame, text=function[0], width=15, height=2, command=function[1])
            button.pack(side="left", padx=10)
            self.function_buttons.append(button)


    def load_beverages(self, filename):
        with open(filename) as f:
            self.beverages = json.load(f)

    def display_menu(self):
        self.clear_frame(self.options_frame)  # Clear the options frame
        # Clear the existing buttons from the options frame
        for button in self.function_buttons:
            button.destroy() # Destroy the button
        self.function_buttons.clear()  # Clear the list of function buttons

        # Create the menu buttons
        self.menu_buttons = []
        for category in self.beverages:
            button = tk.Button(self.options_frame, text=category, width=15, height=2,
                               command=lambda cat=category: self.process_category(cat)) # cat calls the process_category function with the category as the argument
            button.pack(pady=5)
            self.menu_buttons.append(button)
        go_back_button = tk.Button(self.options_frame, text="Go Back",
                                   command=lambda: self.go_back())  # creates a button to go back to the menu
        go_back_button.pack(pady=10)
        self.function_buttons.append(go_back_button) # Add the button to the list of function buttons

    def go_back(self):
        self.options_frame.destroy()  # Destroy the options frame
        self.__init__(self.master)  # Recreate the starting screen
        self.title_label.destroy()  # Destroy the title label


    def process_category(self, category):
        self.clear_frame(self.options_frame) # Clear the options frame

        # Create the category label
        category_label = tk.Label(self.options_frame, text=category, font=("Arial", 14, "bold")) # Create the category label
        category_label.pack(pady=10)

        # Create the beverage buttons
        for beverage in self.beverages[category]:
            beverage_data = self.beverages[category][beverage] # Get the beverage data
            button = tk.Button(self.options_frame, text=beverage, width=15, height=2, #creates a button for each beverage
                               command=lambda b=beverage, bd=beverage_data: self.select_beverage(b, bd))
            button.pack(pady=5)
        go_back_button = tk.Button(self.options_frame, text="Go back", width=13, height=2,command=self.display_menu) #creates a button to go back to the menu
        go_back_button.pack(pady=5)

    def select_beverage(self, beverage, beverage_data):
        messagebox.showinfo("Drink Selection", f"You have chosen {beverage}. Strength: {beverage_data['strength']}") #gets the strength of the beverage and displays it with the beverage name
        self.add_points(self.user, beverage_data['strength'])


    def add_points(self, user, points):
        # Update the user's points in the database
        user.points += points
        session.commit()  # Save the changes to the database
        messagebox.showinfo("Points Earned", f"You have earned {points} points!") #displays the points earned

    def create_profile(self):
        name = simpledialog.askstring("Create Profile", "Enter your name:") #creates a dialog box to enter the name
        age = simpledialog.askinteger("Create Profile", "Enter your age:") #creates a dialog box to enter the age
        if name and age: #if both name and age are entered
            self.db.create_user(name, age) #creates a user with the name and age
            messagebox.showinfo("Profile Created", f"Profile created for {name}.") #displays the name of the user
        else:
            messagebox.showerror("Error", "Invalid input. Please try again.") #if name or age is not entered, displays an error message

    def update_profile(self):
        name = simpledialog.askstring("Update Profile", "Enter your name:")
        if name: #if name is entered
            user = self.db.get_user_by_name(name) #gets the user by name
            if user: #if the user exists
                new_name = simpledialog.askstring("Update Profile",
                                                "Enter your new name (leave blank to keep the current name):") #creates a dialog box to enter the new name
                if new_name is not None: #if the new name is not empty
                    user.name = new_name #updates the name
                    session.commit() #saves the changes to the database
                    messagebox.showinfo("Profile Updated", f"Profile updated for {user.name}.") #displays the name of the user
            else:
                messagebox.showerror("Error", "User not found.") #if the user does not exist, displays an error message
        else:
            messagebox.showerror("Error", "Invalid input. Please try again.") #if name is not entered, displays an error message

    def add_friend(self):
        name = simpledialog.askstring("Add Friend", "Enter your name:")  #creates a dialog box to enter the name
        if name:
            user = self.db.get_user_by_name(name)
            if user: #if the user exists
                friend_name = simpledialog.askstring("Add Friend", "Enter your friend's name:") #creates a dialog box to enter the friend's name
                if friend_name: #if the friend's name is entered
                    friend = self.db.get_user_by_name(friend_name) #gets the friend by name
                    if friend: #if the friend exists
                        self.db.add_friend(user, friend) #adds the friend
                        messagebox.showinfo("Friend Request Sent", f"Friend request sent to {friend.name}.") #displays the name of the friend
                    else: #if the friend does not exist
                        messagebox.showerror("Error", "Friend not found.") #displays an error message
            else: #if the user does not exist
                messagebox.showerror("Error", "User not found.") #displays an error message
        else: #if name is not entered
            messagebox.showerror("Error", "Invalid input. Please try again.") #displays an error message

    def view_friend_requests(self):
        name = simpledialog.askstring("View Friend Requests", "Enter your name:")
        if name:  # if name is entered
            user = self.db.get_user_by_name(name)  # gets the user by name
            if user:  # if the user exists
                friend_requests = self.db.view_friend_requests(user)  # gets the friend requests
                if friend_requests:  # if there are friend requests
                    friend_requests_text = "\n".join(
                        [request.name for request in friend_requests])  # Join the names of friend requests
                    messagebox.showinfo("Friend Requests",
                                        f"Friend requests:\n{friend_requests_text}")  # displays the friend requests
                else:  # if there are no friend requests
                    messagebox.showinfo("Friend Requests",
                                        "You have no friend requests.")  # displays a message saying there are no friend requests
            else:  # if the user does not exist
                messagebox.showerror("Error", "User not found.")  # displays an error message
        else:  # if name is not entered
            messagebox.showerror("Error", "Invalid input. Please try again.")  # displays an error message

    def accept_friend_request(self): #accepts a friend request
        name = simpledialog.askstring("Accept Friend Request", "Enter your name:") #creates a dialog box to enter the name
        if name: #if the name is entered
            user = self.db.get_user_by_name(name) #gets the user by name
            if user:
                friend_name = simpledialog.askstring("Accept Friend Request", "Enter your friend's name:") #creates a dialog box to enter the friend's name
                if friend_name:
                    friend = self.db.get_user_by_name(friend_name) #gets the friend by name
                    if friend: #if the friend exists
                        friendship = session.query(Friendships).filter_by(user_id=friend.id, friend_id=user.id,
                                                                          status="pending").first() #gets the friendship by user id, friend id and status
                        if friendship: #if the friendship exists
                            self.db.accept_friend_request(user, friend) #accepts the friend request
                            messagebox.showinfo("Friend Request Accepted", f"You are now friends with {friend.name}.") #displays the name of the friend
                        else: #if the friendship does not exist
                            messagebox.showerror("Error", "No pending friend request found.") #displays an error message
                    else: #if the friend does not exist
                        messagebox.showerror("Error", "Friend not found.") #displays an error message
                else:   #if the friend's name is not entered
                    messagebox.showerror("Error", "Invalid input. Please try again.") #displays an error message

    def view_friend_list(self):
        name = simpledialog.askstring("View Friend List", "Enter your name:")
        if name:
            user = self.db.get_user_by_name(name)
            if user:
                friends = self.db.get_friends(user) #gets the friends of the user
                if friends: #if the user has friends
                    friend_list = "\n".join([friend.name for friend in friends]) #displays the list of friends
                    messagebox.showinfo("Friend List", f"Friend List:\n{friend_list}") #displays the friend list
                else: #if the user does not have friends
                    messagebox.showinfo("Friend List", "You have no friends yet.") #displays a message that the user has no friends
            else:
                messagebox.showerror("Error", "User not found.")
        else:
            messagebox.showerror("Error", "Invalid input. Please try again.")

    def display_stats(self):
        name = simpledialog.askstring("Display Stats", "Enter your name:")
        if name:
            user = self.db.get_user_by_name(name)
            if user:
                stats = f"Name: {user.name}\nAge: {user.age}\nPoints: {user.points}" #displays the name, age and points of the user
                messagebox.showinfo("Stats", stats) #displays the stats
            else:
                messagebox.showerror("Error", "User not found.")
        else:
            messagebox.showerror("Error", "Invalid input. Please try again.")

    def display_leaderboard(self):
        users = session.query(User).order_by(User.points.desc()).all() #gets the users in descending order of points
        leaderboard = "Leaderboard:\n" #displays the leaderboard
        for index, user in enumerate(users, start=1): #displays the index, name and points of the user
            leaderboard += f"{index}. {user.name} - Points: {user.points}\n"
        messagebox.showinfo("Leaderboard", leaderboard)

    def start_ordering(self):
        name = simpledialog.askstring("Start Ordering", "Enter your name:")
        if name:
            user = self.db.get_user_by_name(name)
            if user: #if the user exists
                self.user = user  #sets the user
                self.display_menu()  #displays the menu
            else:
                messagebox.showerror("Error", "User not found.")
        else:
            messagebox.showerror("Error", "Invalid input. Please try again.")

    def delete_user(self):
        name = simpledialog.askstring("Delete User", "Enter the user's name:")
        if name:
            user = self.db.get_user_by_name(name)
            if user:
                self.db.delete_user(name)
                messagebox.showinfo("User Deleted", f"{name} has been deleted.")
            else:
                messagebox.showerror("Error", "User not found.")
        else:
            messagebox.showerror("Error", "Invalid input. Please try again.")

    def exit_app(self):
        self.master.destroy() #closes the window

    @staticmethod
    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy() #destroys the widgets in the frame

def main():
    root = tk.Tk()
    app = DrinkAndRankGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()