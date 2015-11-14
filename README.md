[![Build Status](https://travis-ci.org/TheSolvingMachine/kangrouter-py.svg?branch=master)](https://travis-ci.org/TheSolvingMachine/kangrouter-py)

# kangrouter-py
Python client for KangRouter. KangRouter is an application for large scale transportation service optimization (see https://thesolvingmachine.com/kangrouter). 
    
## Installation

```bash
pip install kangrouter-py
```

## Usage

### Preliminaries
For interacting with the API, both an *apiKey* and a *licenseId* are required. Please
obtain them from https://thesolvingmachine.com/account.

### An example problem

Input problems are described as a python dict. As a (simplistic) example, consider the problem of taking [Fernando Pessoa](https://en.wikipedia.org/wiki/Fernando_Pessoa) home after a medical appointment at the [Garcia de Orta Hospital](http://www.hgo.pt/). He is ready to leave the hospital after 13:00, but must be home no later than 14:15. Assume that the vehicle available for transportation is parked in [Sintra](https://en.wikipedia.org/wiki/Sintra), has 3 seats and room for 2 wheelchairs. Fernando is on a wheelchair, so we allocate 5 minutes for pickup and dropoff. Additionally, the driver always has a 60 minute lunch break between 12:00 and 14:00.

```python
problem = {
  "nbResources": 2,
  "jobs": [
    {
      "jobId": "Job01",
      "origLat": "38.674921",
      "origLon": "-9.175401",
      "destLat": "38.716860",
      "destLon": "-9.162417",
      "minStartTime": "13:00",
      "maxEndTime": "14:15",
      "pickupDuration": 5,
      "deliveryDuration": 5,
      "cargoId": "Fernando Pessoa",
      "consumptions": [
        0,
        1
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
```
Interesting problems have multiple jobs and multiple vehicles, but the example above should be enough to get you going.

### Submit a problem

The code below creates a new solver for the provided example:

```python
from kangrouter import KangRouterClient
api = KangRouterClient(apiKey,licenseId)
solverId = api.create(problem)
```

### Check solving status

After a solver is created it can be in one of 4 states:
* pending - The solver is queued for execution but not started yet.
* solving - The solver is executing.
* completed - The solver has finished.
* invalid - The problem is invalid, or an unexpected error has occurred.

The function below is used to query the solver current state and obtain information regarding the solving progress:

```python
status = api.getStatus(solverId)
print(status)
```

This is a very simple problem, so the solver executes very quickly:


```python
{
  'execStatus': 'completed',
  'nbJobsDiscarded': 0,
  'solverEndTime': 'Sat Nov 14 20:55:02 2015 GMT',
  'solverStartTime': 'Sat Nov 14 20:54:55 2015 GMT',
  'totalDistance': 75,
  'warnings': [
    {
      'code': 5, 
      'info': "Unpaired job 'Job01'."
    }
  ]
}
```

Given that larger problems may take a few minutes, calling this function while the solver is executing will also return ETA (expected delivery time) for completion.

### Get the solution

When the solver is done, the solution may be retrieved as follows:

```python
solution = api.getSolution(solverId)
print(solution)
```

The solution shows at what times, or time intervals, drivers must leave their depots, start their work breaks, or perform pickup/delivery actions:

```python
{
  'jobsScheduled': [
    {
      'jobId': 'Job01',
      'maxEndTime': '14:15',
      'maxStartTime': '13:55',
      'minEndTime': '13:20',
      'minStartTime': '13:00',
      'vehicleId': '12-AS-46'
    }
  ],
  'type': 'total',
  'vehiclesScheduled': [
    {
      'breaks': [
        {
          'breakId': 'Lunch',
          'maxEndTime': '13:55',
          'maxStartTime': '12:55',
          'minEndTime': '13:00',
          'minStartTime': '12:00'
        }
      ],
      'maxEndTime': '21:30',
      'maxStartTime': '12:30',
      'minEndTime': '13:40',
      'minStartTime': '07:00',
      'vehicleId': u'12-AS-46'
    }
  ]
}
```
### Other methods
The remaining methods allow to stop a running solver, which might be useful if you're in a hurry:

```python
api.stop(solverId)
```

and remove a solver (and associated data) from the server:

```python
api.delete(solverId)
```

## More documentation
For a complete description of the KangRouter API please visit https://thesolvingmachine.com/swagger/kangrouter/srv/.
