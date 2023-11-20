# MuberApp
MuberApp is a basic implementation of uber app


## Muber app is platform that lets registered passengers to add like/dislike to registered drivers.


## To interact with the API, utilize following endpoints:

```
""                        supports [get] method/s                     authentication_classes = [], permission_classes=[]
"passengers/register/"    supports [post] method/s                    authentication_classes = [], permission_classes=[]
"passengers/login/"       supports [post] method/s                    authentication_classes = [], permission_classes=[]
"passengers/detail/"      supports [get, patch] method/s              authentication_classes = [JSONWebTokenAuthentication], permission_classes=[]
"passengers/drivers/"     supports [get] method/s                     authentication_classes = [JSONWebTokenAuthentication], permission_classes=[]
"passengers/like/"        supports [post] method/s                    authentication_classes = [JSONWebTokenAuthentication], permission_classes=[IsPremiumPassenger]
"drivers/register/"       supports [post] method/s                    authentication_classes = [], permission_classes=[]
"drivers/login/"          supports [post] method/s                    authentication_classes = [],  permission_classes = []
"drivers/detail/"         supports [get, patch] method/s               authentication_classes = [JSONWebTokenAuthentication], permission_classes=[]
"drivers/delete/"         supports [delete] method/s                  authentication_classes = [JSONWebTokenAuthentication], permission_classes=[]
"passengers/delete/"      supports [delete] method/s                  authentication_classes = [JSONWebTokenAuthentication], permission_classes=[]


```

## Endpoint descriptions
----------------------------------
## "" (home)
```
Send a get request to get the details of api endpoints. 
```
----------------------------------
## passengers/register/   
```
Send a post request to register a passenger. Creates a passenger instance and sets his total_rides to 0
Format:
{
    "user": {
        "username":  "passenger1",
        "password": "password123"
    },
    "age": 21
}
```
----------------------------------
## passengers/login/
### Each login increases the user's total_rides by 1
```
Send a post request to log in as a passenger. Returns a jwt token to be utilized for other endpoints that require [JSONWebTokenAuthentication]
Format:
{
            "username": "passenger1",
            "password": "password123"
        }

```
----------------------------------
## passengers/detail/
```
Requires [JSONWebTokenAuthentication].
Send a get request to fetch the user's details.
Send a patch request to update the user's details.
Format:
{"user":{
        "username":  "passenger1",
        "password": "password123"
    },
"age": 19}  
```
----------------------------------
## passengers/drivers/
```
Requires [JSONWebTokenAuthentication].
Send a get request to fetch all available drivers.
```
----------------------------------
## drivers/register/
```
Send a post request to register a driver.
Format:
{
    "name": {
        "username":  "driver1",
        "password": "password123"
    },
    "car_model": "Hondacity",
    "age":23,
    "languages":"UR"
}
Creates a driver instance and sets the read-only attributes "positive_likes","negative_likes" to 0.
LANGUAGES = [
        ('EN', 'English'),
        ('UR', 'Urdu'),
        ('HI', 'Hindi'),
        ('OT', 'Others'),
    ]
```
----------------------------------
## drivers/login/
```
Send a post request to log a driver in.
Format:
{
            "username": "driver1",
            "password": "password123"
        }

```
----------------------------------

## drivers/detail/
```
Requires [JSONWebTokenAuthentication].
Send a get request to fetch the driver's details.

Send a patch request to update the driver's details.
Format:
{
"name":
    {"username":"driver1","password":"passowrd123"},
"age": 35,
"car_model":"Audi",
"languages": "EN"
}
```
----------------------------------
## passengers/like/

```
IsPremiumPassenger : A passenger upgrades to Premium if his total_rides are greater than 3.


Requires authentication_classes = [JSONWebTokenAuthentication], permission_classes = [IsPremiumPassenger]
IsPremiumPassenger : A passenger upgrades to Premium if his total_rides are greater than 3.
Send a post request with driver username and either a 'like':'+' or a 'dislike':'-'
Format:
{
"username":"driver1",
"dislike":"-"

}
or
{
"username":"driver1",
"like":"+"

}
```
----------------------------------
## "drivers/delete/"
```
Requires authentication_classes = [JSONWebTokenAuthentication], permission_classes = []
Send a delete request to delete a driver.

```
----------------------------------
## passengers/delete/"
```
Requires authentication_classes = [JSONWebTokenAuthentication], permission_classes = []
Send a delete request to delete a passenger.

```
----------------------------------


