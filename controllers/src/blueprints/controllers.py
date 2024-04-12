from flask import jsonify, request, Blueprint
from ..commands.saveEmail import CreateEmail
from ..commands.searchEmail import SearchEmail
from ..errors.errors import FatalError

controllersBlueprint = Blueprint("blacklists", __name__)

@controllersBlueprint.route("/blacklists", methods=["POST"])
def postEmailBlackList():
  try:
    authorizationToken = request.headers.get("Authorization")
    token = None
    if authorizationToken is not None:
      token = authorizationToken.replace("Bearer ", "")
      
    json_data = request.get_json()
    email = json_data.get("email")
    appUuid = json_data.get("app_uuid")
    blockedReason = json_data.get("blocked_reason")
    
    base = CreateEmail(
      email=email,
      appUuid=appUuid,
      blockedReason=blockedReason,
      token=token
    ).execute()
    return jsonify({ "msg": base["msg"] }), 201
  except FatalError as error:
    return jsonify({"error": str(error.description)}), error.code

@controllersBlueprint.route("/blacklists/<email>", methods=["GET"])
def getEmailBlackList(email):
  try:
    authorizationToken = request.headers.get("Authorization")
    token = None
    if authorizationToken is not None:
      token = authorizationToken.replace("Bearer ", "")
    baseInfo = SearchEmail(email=email, token=token).execute()
    if baseInfo:
      return jsonify(baseInfo), 200
  except FatalError as error:
    return jsonify({"error": str(error.description)}), error.code
