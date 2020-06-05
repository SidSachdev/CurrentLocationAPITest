### Current Location API Service

An Location API Service Test to detect fraud.

This is a Python [Flask](https://flask.palletsprojects.com/en/1.1.x/) application that uses [Gunicorn](https://gunicorn.org)
Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. 
The application is currently hosted on AWS ElasticBeanstalk and is using Postgres

For the Fuzzy Substring match the application uses [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy)
An open source application created by SeatGeek and it uses Levenshtein Distance to calculate ratios
The threshold for the ratio substring match is set to 50 by default. Configurable through environment.

## Setup:

Clone the repo (file provided)

Create a new [virtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/) with Python 3.5+

Activate the new environment

Install the requirements.txt file: 

```
pip install -r requirements.txt
```

Run the application locally using:

```
gunicorn -b 0.0.0.0:8000 -k gthread --thread=4 -w=1 app:app
```

## Usage 

# Submit a visit

```
POST /users/{userId}/visits
Example (for local use (0.0.0.0:8000))

Enter your params below

CURL: 

curl --location --request POST 'https://currentlocationapi.sidsachdev.com/api/v1/users/{user_id}/visits' \
--header 'Content-Type: application/json' \
--data-raw '{
    "merchant": {
        "merchantId": "{merchant_id}",
        "merchantName": "{merchant_name}"
    },
    "user": {
        "userId": "{user_id}"
    }
}'



```

# Retrieve a list of potential visits by userId and a search string

```
GET /users/{userId}/visits?searchString=X
Example
CURL:

curl --location --request GET 'https://currentlocationapi.sidsachdev.com/api/v1/users/1/visits?searchString=CHELSEA'



GET /users/1/visits?searchString=CHELSEA

Returns:
[
    {
        "merchant": {
            "merchantId": "5ed40522965aae879ab22d0995215",
            "merchantName": "CHELSEA"
        },
        "timestamp": 1590986974,
        "user": {
            "userId": "1"
        },
        "visitId": "3d3a52e7-8412-4c8b-8a43-140d664889c7"
    },....

] 
    

```

# Retrieve a single visit by visitId

```
GET /visits/{visitId}
Example

GET /visits/3d3a52e7-8412-4c8b-8a43-140d664889c7

CURL:

curl --location --request GET 'https://currentlocationapi.sidsachdev.com/api/v1/visit/3d3a52e7-8412-4c8b-8a43-140d664889c7'


Returns:
{
    "merchant": {
        "merchantId": "5ed40522965aae879ab22d0995215",
        "merchantName": "CHELSEA"
    },
    "timestamp": 1590986974,
    "user": {
        "userId": "1"
    },
    "visitId": "3d3a52e7-8412-4c8b-8a43-140d664889c7"
}
```


## License
[MIT](https://choosealicense.com/licenses/mit/)

author = "Sid Sachdev"
email = "sid.sachdev9 (AT) gmail (DOT) com"