class ApiError(Exception):
  code = 422
  description = "Default message"
  
class FatalError(ApiError):
  code = 500
  description = "Estamos presentando fallas t\u00e9cnicas. Por favor intenta m\u00e1s tarde"

class RequestFieldEmpty(ApiError):
  code = 400
  description = "Se deben ingresar todos los par\u00e1metros"

class RequestFieldNotString(ApiError):
  code = 400
  description = "Los par\u00e1metros deben ser de tipo string"

class InvalidUuidFormat(ApiError):
  code = 400
  description = "El app_uuid no tiene el formato correspondiente"

class TokenNoValid(ApiError):
  code = 401
  description = "El token no es v\u00e1lido"

class TokenEmpty(ApiError):
  code = 403
  description = "Token vac\u00edo"

class EmailNotExist(ApiError):
  code = 404
  description = "El correo no existe"

class EmailAlreadyExist(ApiError):
  code = 412
  description = "El correo ya existe"
