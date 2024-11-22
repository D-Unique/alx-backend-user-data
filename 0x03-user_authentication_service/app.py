#!/usr/bin/env python3
"""This module contain the flask app"""
from flask import Flask, render_template, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """ Home route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        abort(400)
    return jsonify({"message": "email already registered"})


@app.route("/sessions", methods=['POST'])
def login():
    """
    login method
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response_payload = {
            "email": email,
            "message": "logged in"
        }
        response = jsonify(response_payload)
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
