from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Boolean, Integer, DateTime, func, ForeignKey, Enum, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# For use a selective value, this case, male y female, we the imported method Enum, from my sqlaclhemy
gender_state = Enum('male', 'female', name='gender_enum')


class User(db.Model):
    __tablename__ = "users"
    users_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    fisrt_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)


class Character(db.Model):
    __tablename__ = "characters"
    characters_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(250), nullable=False)
    gender: Mapped[str] = mapped_column(gender_state, nullable=False)
    # That's how we created an automated date. For Create and update datetime record.
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    update_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now())


class Planet(db.Model):
    __tablename__ = "planets"
    planets_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    population: Mapped[int] = mapped_column(Integer, nullable=True)
    terrain: Mapped[str] = mapped_column(String(250), nullable=False)
    # The characters live in planets
    who_live_here: Mapped[int] = mapped_column(
        ForeignKey('characters.characters_id'), nullable=True)


class Favorite(db.Model):
    __tablename__ = "favorites"
    favorites_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # The user can save as favorite planets and characteres. In order to get a good record the user only can save 1 planet or 1 characteer
    users_id: Mapped[int] = mapped_column(
        ForeignKey('users.users_id'), nullable=False)
    # The typing Optional allows you to put another type of data instead of int. We switch nullable to true in order
    # to accept the argument value null or not after these lines
    planets_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('planets.planets_id'), nullable=True)
    characters_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('characters.characters_id'), nullable=True)
    __table_args__ = (
        # In these lines we define where character and planet are null or not, in order to choose one option
        CheckConstraint(
            '(characters_id IS NOT NULL AND planets_id IS NULL) OR (characters_id IS NULL AND planets_id IS NOT NULL)',
            name='check_one_favorite_type'
        ),
    )

# Favorites
# --
# id int pk
# user_id int FK >- User.id
# characters_id int FK >- Characters.id
# planets_id int FK >- Planets.id

# User
# --
# id int pk
# email string unique
# fisrt_name varchar(250)
# last_name string
# password string(128)

# Characters
# --
# id int pk FK >- Planets.characters_id
# name varchar(250)
# birth_year string
# gender string
# created_at date
# update_at date

# Planets
# --
# id int pk
# name varchar(250)
# population int
# terrain string
# characters_id int FK
