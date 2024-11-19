#!/usr/bin/env python3
"""This module contain the flask app"""
from flask import Flask, render_template, jsonify
from auth import Auth


app = Flask(__name__)
AUTH = Auth()

@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """ Home route"""
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user(email: str, password: bytes):
    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({"email": {email}, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
