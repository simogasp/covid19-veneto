# Json data

The data is a "dump" of python dictionary that collects the data with a similar structure both for the `provinces` and the `hospitals`

## Provinces

This contains the daily number of people that are positive and those that are in isolation.
The structure of the json is as follows:

```json
{
    # the list of dates that has been collected
    "dates" : ["20200306",  "20200306", ...]
    
    # this contains the data for all cities
    "places" : 
    {
        # name of the city
        "city1" : 
        {
            # people in isolation, a dict with date as key and the daily number of people in isolation as value
            "isolamento" : {"20200306": 2,  "20200306": 3, ...}
            # positives, a dict with date as key and the daily number of positive persons
            "totale positivi" : {"20200306": 45,  "20200306": 76, ...}
        } 

        "city2" : 
        {
            "isolamento" : {"20200306": 0,  "20200306": 12, ...}
            "totale positivi" : {"20200306": 56,  "20200306": 132, ...}
        }     
   
    } 
}
```

## Hospitals

The structure of the hospital data is fairly similar:

```json
{
    # the list of dates that has been collected
    "dates" : ["20200306",  "20200306", ...]
    
    # this contains the data for all hospitals
    "hospitals" : 
    {
        # name of the hospital
        "hospital1" : 
        {
            # deaths, a dict with date as key and the cumulative number of death patients
            "decessi" : {"20200306": 2,  "20200306": 3, ...}
            # discharged, a dict with date as key and the cumulative number of discharged patients
            "dimessi" : {"20200306": 45,  "20200306": 76, ...}
            # hospitalized people in non critical conditions, a dict with date as key and the daily number of people 
            "non critici" : {"20200306": 2,  "20200306": 3, ...}
            # patients in intensive care, a dict with date as key and the daily number patients in intensive care
            "terapia intensiva" : {"20200306": 45,  "20200306": 76, ...}

        } 

        "hospital2" : 
        {
            "decessi" : {"20200306": 2,  "20200306": 3, ...}
            "dimessi" : {"20200306": 45,  "20200306": 76, ...}
            "non critici" : {"20200306": 2,  "20200306": 3, ...}
            "terapia intensiva" : {"20200306": 45,  "20200306": 76, ...}
        }     
   
    } 
}
```