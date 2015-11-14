
from kangrouter import KangRouterClient
import time
import os

apiKey = os.environ["API_KEY"]
licenseId = os.environ["LICENSE_ID"]

problem = {
  "nbResources": 3,
  "jobs": [
    {
      "jobId": "Job01",
      "origLat": "38.674921",
      "origLon": "-9.175401",
      "destLat": "38.716860",
      "destLon": "-9.162417",
      "minStartTime": "13:00",
      "maxStartTime": "13:15",
      "minEndTime": "13:55",
      "maxEndTime": "13:55",
      "pickupDuration": 10,
      "deliveryDuration": 10,
      "cargoId": "Fernando Pessoa",
      "consumptions": [
        0,
        1,
        0
      ]
    }
  ],
  "vehicles": [
    {
      "vehicleId": "12-AS-46",
      "depotLat": "38.806842",
      "depotLon": "-9.382556",
      "minStartTime": "07:00",
      "maxEndTime": "22:00",
      "maxWorkDuration": 540,
      "capacities": [
        2,
        3,
        0
      ],
      "breaks": [
        {
          "breakId": "Lunch",
          "minStartTime": "12:00",
          "maxEndTime": "14:00",
          "duration": 60
        }
      ],
      "overspeed": 1.25
    }
  ]
}

def test():
  api = KangRouterClient(apiKey,licenseId)
  solverId = api.create(problem)
  status = api.getStatus(solverId)
  solution = api.getSolution(solverId)
  time.sleep(10)
  status = api.getStatus(solverId)
  assert status["execStatus"]=="completed"
  assert status["totalDistance"]==75
  solution = api.getSolution(solverId)
  assert solution["type"]=="total"
  assert len(solution["jobsScheduled"])==1
  