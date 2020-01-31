# Flask App

## Table of Contents
1. [Get up and running](#get-up-and-running)
2. [Curl Samples](#curl-samples)
3. [Running tests](#running-tests)


### Get up and running
1- Spin up backend docker container by running:
```shell script
$ docker-compose up
```

2- Navigate API using Swagger UI by visiting
```
http://localhost:5000/swagger/
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
```shell script
# activate venv
$ source venv/bin/activate 
```
```shell script
$ cd services/tests 
```
```shell script
# run tests
$ python -m pytest 
```  


