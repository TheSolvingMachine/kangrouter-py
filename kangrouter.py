import time

from tsm.common.app import exception

import requests
import json
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

KANGROUTER_WEBSERVICE_APPLICATION_ROOT="/kangrouter/srv/v1"

class KangRouterClient:
  pathbase = "https://thesolvingmachine.com/kangrouter/srv/v1/solvers"
  def __init__(self,apiKey,licenseId):    
    self.headers = {"content-type": "application/json",
                    "Authorization": apiKey}
    self.params = {"licenseId" : licenseId }
    retries = Retry(total=5,
                    backoff_factor=0.75)
    self.session = requests.Session()
    self.session.mount(KANGROUTER_WEBSERVICE_APPLICATION_ROOT, 
                       HTTPAdapter(max_retries=retries))

  def validateReply(self,req):
    if req.status_code >= 400 and req.status_code <= 500:
      try:
        j = req.json()
      except ValueError:
        raise exception.InternalError(req.text,req.status_code)
      raise exception.jsonToException(req.json())

  def create(self,problem,**kwargs):
    path = self.pathbase
    payload=json.dumps(problem)
    params = self.params.copy()
    params.update(kwargs)
    req = self.session.post(path,
                        params=params, 
                        headers=self.headers,
                        data=payload)    
    self.validateReply(req)
    return req.text
    
  def delete(self,solverId):
    path = "{base}/{solverId}".format(base=self.pathbase,
                                      solverId=str(solverId))
    req = self.session.delete(path,
                          params=self.params,
                          headers=self.headers)
    self.validateReply(req)
    return True
    
  def stop(self,solverId):
    path = "{base}/{solverId}/stop".format(base=self.pathbase,
                                      solverId=str(solverId))
    req = self.session.put(path,
                       params=self.params,
                       headers=self.headers)
    self.validateReply(req)
    return True
    
  def getStatus(self,solverId):
    path = "{base}/{solverId}/status".format(base=self.pathbase,
                                      solverId=str(solverId))
    req = self.session.get(path,
                       params=self.params,
                       headers=self.headers)
    self.validateReply(req)
    return req.json()

  def getSolution(self,solverId):
    path = "{base}/{solverId}/solution".format(base=self.pathbase,
                                      solverId=str(solverId))
    req = self.session.get(path,
                       params=self.params,
                       headers=self.headers)
    self.validateReply(req)
    return req.json()
    
  # polling 
  def createAndWait(self,problem,cancel,**kwargs):
    solverId = self.create(problem,**kwargs)
    timeout = 300
    while not cancel() and timeout>0:
      status = self.getStatus(solverId)
      if status["execStatus"] =="invalid":
        raise exception.solverError(json.dumps(status["errors"]))
      if status["execStatus"] =="completed":
        return self.getSolution(solverId)
      time.sleep(1)
      timeout -= 1
    if timeout == 0:
      raise exception.InternalError("Timed out waiting for solver")
    raise exception.UserCancelled()
    

    
