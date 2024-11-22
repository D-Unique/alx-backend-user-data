#!/usr/bin/env python3
"""This module contain the flask app"""
from flask import Flask, render_template, jsonify, request, abort
from flask import redirect, url_for
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


@app.route("/sessions", methods=['DELETE'])
def logout():
    """logout route"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('home'), code=302)
    else:
        abort(403)


@app.route("/profile", methods=['GET'])
def profile():
    """view profile"""
    session_id = request.cookies.get('session_id')
    if session_id:
        users = AUTH.get_user_from_session_id(session_id)
        if users:
            response = jsonify({"email": users.email})
            return response
        else:
            abort(403)
    else:
        abort(403)


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """
    get_reset_password_token
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        response = jsonify({"email": email, "reset_token": reset_token})
        return response
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """
    update password
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
        response = jsonify({"email": email, "message": "Password updated"})
        return response
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
