from datetime import datetime

import flask_login
from flask import request
from sqlalchemy import REAL, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from modules import database


class User(flask_login.UserMixin, database.Model):
    __tablename__ = "users"

    email = Column(String, primary_key=True)
    firm_id = Column(Integer, ForeignKey("firms.firm_id"), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    password_hashed = Column(String(128), nullable=False)
    created_on = Column(DateTime(), nullable=False)
    role = Column(String(), nullable=False)

    # Relationship with Firm
    firm = relationship("Firm", back_populates="users")

    def __init__(
        self, email: str, first_name: str, last_name: str, password: str, role: str
    ):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hashed = self._generate_password_hash(password)
        self.created_on = datetime.now()
        self.role = role

    def get_id(self):
        return self.email

    def update(self, request: request):
        self.email = request.form["email"]
        self.password_hashed = self._generate_password_hash(request.form["password"])
        self.first_name = request.form["fname"]
        self.last_name = request.form["lname"]
        self.role = request.form["role"]

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)


class Firm(database.Model):
    __tablename__ = "firms"

    firm_id = Column(Integer, primary_key=True)
    firm_name = Column(String, nullable=False, unique=True)

    # Relationship with User
    users = relationship("User", back_populates="firm")

