import pytest
import json
from services import app, model, request_validator, routes
import os


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # adds JWT token to client to be used by tests that need it
        client.jwt_token = get_jwt_token()
        yield client


def get_jwt_token():
    test_client = app.test_client()
    res = test_client.post('/authenticate', data=json.dumps({
        "jwt_secret": "jwt_secret"
    }), content_type='application/json')
    jwt_token = res.json['jwt']
    return jwt_token


def test_get_services_ok(client):
    res = client.get('/services')
    assert res.data != {}
    assert res.status_code == 200


def test_put_new_service(client):
    res = client.put('/services', data=json.dumps(put_data_new),
                     headers={'Authorization': "Bearer " + client.jwt_token},
                     content_type='application/json')
    assert res.status_code == 201
    assert res.json['message'] == 'Service Created'


def test_put_update_service(client):
    res = client.put('/services', data=json.dumps(put_data_update),
                     headers={'Authorization': "Bearer " + client.jwt_token},
                     content_type='application/json')
    assert res.status_code == 200
    assert 'Service Updated' in res.json['message']


def test_put_service_invalid_request(client):
    res = client.put('/services', data={}, headers={'Authorization': "Bearer " + client.jwt_token})
    assert res.status_code == 400
    assert res.json['message'] == 'payload must be a valid json'


def test_put_service_invalid_schema_missing_key(client):
    res = client.put('/services', data=json.dumps(put_data_missing_key_error),
                     headers={'Authorization': "Bearer " + client.jwt_token},
                     content_type='application/json')
    assert res.status_code == 400
    assert "Missing key" in res.json['message']


def test_put_service_invalid_schema_wrong_key(client):
    res = client.put('/services', data=json.dumps(put_data_wrong_key_error),
                     headers={'Authorization': "Bearer " + client.jwt_token},
                     content_type='application/json')
    assert res.status_code == 400
    assert "Wrong key" in res.json['message']


def test_put_no_jwt_token(client):
    res = client.put('/services', data=json.dumps(put_data_update),
                     content_type='application/json')
    assert res.status_code == 401
    assert 'Missing Authorization Header' in res.json['msg']


def test_auth_missing_jwt(client):
    res = client.post('/authenticate', data=json.dumps({
        "": "jwt_secret"
    }), content_type='application/json')
    assert res.status_code == 400
    assert 'Missing jwt_secret parameter' in res.json['message']


def test_auth_bad_secret(client):
    res = client.post('/authenticate', data=json.dumps({
        "jwt_secret": "xyz"
    }), content_type='application/json')
    assert res.status_code == 401
    assert 'Bad jwt_secret' in res.json['message']


@pytest.fixture(autouse=True)
def run_around_tests():
    # restores the initial JSON DB in file system after tests are ran
    data_before = load_data_from_db('fresh_db.json')
    yield
    persist_data_in_db('db.json', data_before)


def load_data_from_db(filename):
    with open(os.path.join('static', filename)) as file:
        data = json.load(file)
        return data


def persist_data_in_db(filename, data):
    with open(os.path.join('static', filename), 'w') as file:
        json.dump(data, file, indent=2)


put_data_new = {
    "service": "Service NEW",
    "ip": "10.75.53.100",
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
}

put_data_update = {
    "service": "Service I",
    "ip": "10.75.53.100",
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
}

put_data_wrong_key_error = {
    "service": "Service I",
    "ip": "10.75.53.100",
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
    ],
    "jibberish": "morejibberish",
}

put_data_missing_key_error = {
    "ip": "10.75.53.100",
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
}
