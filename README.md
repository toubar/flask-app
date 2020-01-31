# Flask App

## Table of Contents
1. [Get up and running](#get-up-and-running)
2. [Curl Samples](#curl-samples)
3. [Running tests](#running-tests)


### Get up and running

#### Docker
1- Spin up backend docker container by running:
```shell script
$ docker-compose up
```

2- Navigate API using Swagger UI by visiting [the URL below](http://localhost:5000/swagger/)
```
http://localhost:5000/swagger/
```

#### Manually
1. clone this repo
```shell script
$ git clone https://github.com/toubar/flask-app backend
```

2. create python virtual environement
```shell script
$ python -m venv venv
```

3. install dependencies
```shell script
$ venv/bin/pip install -r requirements.txt
```

4. activate virtualenv
```shell script
$ source venv/bin/activate
```

5. add Flask env variables
```shell script
$ export FLASK_APP="main.py"
```
```shell script
$ export FLASK_ENV="development"
```
```shell script
$ export FLASK_DEBUG=True
```

6. spin up flask server
```shell script
$ venv/bin/python -m flask run
```

### Curl Samples
GET Services
```shell script
curl --request GET \
  --url http://127.0.0.1:5000/service
```

POST Auth (for JWT token)
```shell script
curl --request POST \
  --url http://127.0.0.1:5000/authenticate \
  --header 'authorization: Bearer undefined' \
  --header 'content-type: application/json' \
  --data '{
	  "jwt_secret": "jwt_secret"
}'
```

PUT Service (new) -- get JWT token from Auth endpoint
```shell script
curl --request PUT \
  --url http://127.0.0.1:5000/services \
  --header 'authorization: Bearer <<<PUT JWT TOKEN HERE>>>' \
  --header 'content-type: application/json' \
  --data '{
	  "service": "New Service",
    "ip": "10.12.99.264",
    "servers": [
        {
            "name": "lin-brn-891",
            "status": "running"
        },
        {
            "name": "lin-brn-125",
            "status": "error"
        },
        {
            "name": "lin-brn-711",
            "status": "running"
        },
        {
            "name": "lin-brn-999",
            "status": "running"
        }
    ]
}'
```


### Running tests

assuming venv is activated...

```shell script
$ cd services/tests 
```

```shell script
# run tests
$ python -m pytest 
```  


