from dotenv import load_dotenv
loaded = load_dotenv('.env.development')

from flask import Flask, jsonify
from .blueprints.controllers import controllersBlueprint
from .errors.errors import ApiError
import os

app = Flask(__name__)
app.register_blueprint(controllersBlueprint)

@app.errorhandler(ApiError)
def handle_exception(err):
  response = {
    "msg": err.description,
    "version": os.getenv("VERSION", "1.0")
  }
  return jsonify(response), err.code
