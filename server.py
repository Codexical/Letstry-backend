# import libraries
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flasgger import Swagger
import json, os

# init files
if os.path.exists("storage/users.json"):
    with open("storage/users.json", "r") as f:
        users = json.load(f)
else:
    users = {"test": {"ID": 0, "username": "aura", "password": "test"}}


app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "Letstry system API",
    "description": "This is the API for the Letstry system",
    "version": "1.0.0",
    "hide_top_bar": True,
}
CORS(app)
Swagger(app)


@app.route("/health", methods=["POST"])
def health():
    """
    Health check
    ---
    responses:
      200:
        description: OK
        examples:
            application/json: {"status": "ok"}
    """
    return Response(
        json.dumps({"status": "ok"}), status=200, mimetype="application/json"
    )


@app.route("/login", methods=["POST"])
def login():
    """
    Login
    ---
    parameters:
      - name: account
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    responses:
        200:
            description: OK
            examples:
                application/json: {"status": "ok", "ID": 0, "username": "name"}
        400:
            description: Password incorrect
            examples:
                application/json: {"status": "Password incorrect"}
        400:
            description: No user found
            examples:
                application/json: {"status": "No user found"}

    """
    account = request.values["account"]
    password = request.values["password"]
    if account in users:
        if users[account]["password"] == password:
            return Response(
                json.dumps(
                    {
                        "status": "ok",
                        "ID": users[account]["ID"],
                        "username": users[account]["username"],
                    }
                ),
                status=200,
                mimetype="application/json",
            )
        else:
            return Response(
                json.dumps({"status": "Password incorrect"}),
                status=400,
                mimetype="application/json",
            )
    else:
        return Response(
            json.dumps({"status": "No user found"}),
            status=400,
            mimetype="application/json",
        )


@app.route("/create", methods=["POST"])
def create():
    """
    Create a new user
    ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: account
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    responses:
        200:
            description: OK
            examples:
                application/json: {"status": "ok", "ID": 0, "username": "name"}
        400:
            description: User already exists
            examples:
                application/json: {"status": "User already exists"}
    """
    username = request.values["username"]
    account = request.values["account"]
    password = request.values["password"]
    if account in users:
        return Response(
            json.dumps({"status": "User already exists"}),
            status=400,
            mimetype="application/json",
        )
    else:
        users[account] = {
            "ID": len(users),
            "username": username,
            "password": password,
        }
        with open("storage/users.json", "w") as f:
            json.dump(users, f, indent=4)
        return Response(
            json.dumps(
                {
                    "status": "ok",
                    "ID": users[account]["ID"],
                    "username": users[account]["username"],
                }
            ),
            status=200,
            mimetype="application/json",
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
