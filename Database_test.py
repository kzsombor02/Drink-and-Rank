from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    points = Column(Integer)

    def __repr__(self):
        return f"User(name={self.name}, age={self.age}, points={self.points})" # returns the name, age and points of the user




class Friendships(Base):
    __tablename__ = "friendships"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    friend_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    status = Column(String)

    def __repr__(self):
        return f"Friendships(user_id={self.user_id}, friend_id={self.friend_id}, status={self.status})" # returns the status of the friendship


class Drink(Base):
    __tablename__ = "drinks"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    strength = Column(Integer)

    def __repr__(self):
        return f"Drink(name={self.name}, strength={self.strength})" # returns the name and strength of the drink


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="ratings") # making a relationship between the Rating and User table
    drink_id = Column(Integer, ForeignKey('drinks.id'))
    drink = relationship("Drink", backref="ratings") # making a relationship between the Rating and Drink table
    rating = Column(Integer)

    def __repr__(self):
        return f"Rating(user_id={self.user_id}, drink_id={self.drink_id}, rating={self.rating})" # returns the rating of the user

engine = create_engine('sqlite:///assignment_database.db') # creating the database
Base.metadata.create_all(engine) # creating the tables
Session = sessionmaker(bind=engine) # creating a session
session = Session() # creating a session


