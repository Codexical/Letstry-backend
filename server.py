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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
