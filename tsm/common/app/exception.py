
ERROR_INVALID_API_USAGE = 1
ERROR_INTERNAL = 2
ERROR_USER_CANCELLED = 3
ERROR_GEOCODER = 4

errors = { ERROR_INVALID_API_USAGE : "Invalid API usage.",
       ERROR_INTERNAL : "Internal error.",
       ERROR_USER_CANCELLED : "Cancelled by user.",
       ERROR_GEOCODER : "Geocoder error."}

class MultipleInvalidAPIUsage(Exception):
  pass

class InvalidAPIUsage(Exception):
  status_code = 400
  code = ERROR_INVALID_API_USAGE
  def __init__(self, message, status_code=None, payload=None):
    Exception.__init__(self)
    self.message = message
    if status_code is not None:
      self.status_code = status_code
    self.payload = payload

  def format(self,**data):
    self.message = self.message.format(**data)
    return self
  
  def to_dict(self, showXInfo=True):
    rv = {"code" : self.code,
        "error" : errors[ERROR_INVALID_API_USAGE],
        "info" : self.message}
    return rv
  
  def __str__(self):
    return "Invalid API Usage: "+self.message+" (status_code="+str(self.status_code)+")"
  
class InternalError(Exception):
  code = ERROR_INTERNAL
  def __init__(self, message,status_code=500):
    Exception.__init__(self)
    self.status_code = status_code
    self.message = message
  def to_dict(self):
    rv = {"code" : self.code,
        "error" : errors[ERROR_INTERNAL],
        "info" : self.message}
    return rv
  def __str__(self):
    return "Internal Error ("+str(self.status_code)+") :"+str(self.message)
  
class UserCancelled(Exception):
  code = ERROR_USER_CANCELLED
  def __init__(self, message=""):
    Exception.__init__(self)
    self.message = message
  def to_dict(self):
    rv = {"code" : self.code,
        "error" : errors[ERROR_USER_CANCELLED],
        "info" : self.message}
    return rv

class GeocoderError(Exception):
  """Exception raised for errors in geocoding service.
  Attributes:
    msg  -- server message
  """
  status_code = 500
  code = ERROR_GEOCODER
  def __init__(self, message=""):
    Exception.__init__(self)
    self.message = message
  def __str__(self):
    return self.message
  def to_dict(self):
    rv = {"code" : self.code,
        "error" : errors[ERROR_GEOCODER],
        "info" : self.message}
    return rv

def jsonToException(d):
  if d["code"] == ERROR_INTERNAL:
    return InternalError(d["info"])
  elif d["code"] == ERROR_USER_CANCELLED:
    return UserCancelled(d["info"])
  elif d["code"] == ERROR_GEOCODER:
    return GeocoderError(d["info"])
  else:
    return InvalidAPIUsage(d["info"],d["code"])
