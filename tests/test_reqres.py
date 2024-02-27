import json
import requests
from jsonschema import validate

from support.schemas_path import load_schema


def test_get_user(base_url):
    first_name = "Lindsay"
    last_name = "Ferguson"
    response = requests.get(f"{base_url}/users", data={"name": first_name, "last_name": last_name})

    assert response.status_code == 200


def test_update_user(base_url):
    name = "Diana"
    job = "Doctor"
    response = requests.put(f"{base_url}/users/2", data={"name": name, "job": job})

    assert response.status_code == 200
    assert response.json()["name"] == name
    assert response.json()["job"] == job
    assert response.json()["job"] != ["name"]


def test_user_not_found(base_url):
    response = requests.get(f"{base_url}/users/23")

    assert response.status_code == 404
    body = response.json()

    assert body == {}


def test_delete_user(base_url):
    response = requests.delete(f"{base_url}/users/2")
    print(response.text)
    assert response.text == ''


def test_user_login_success(base_url):
    email = "eve.holt@reqres.in"
    password = "cityslicka"
    response = requests.post(f"{base_url}/login", data={"email": email, "password": password})
    body = response.json()

    assert body["token"] == "QpwL5tke4Pnpja7X4"
    schema = load_schema("login_user.json")
    with open(schema) as file:
        schema = json.load(file)
    validate(body, schema=schema)


def test_create_user(base_url):
    name = "morpheus"
    job = "leader"

    response = requests.post(f"{base_url}/users", data={"name": name, "job": job})
    body = response.json()

    assert response.status_code == 201

    schema = load_schema("create_user.json")
    with open(schema) as file:
        schema = json.load(file)
    validate(body, schema=schema)

    assert body["name"] == name
    assert body["job"] == job


def test_user_list(base_url):
    first_name = "Tobias"
    last_name = "Funke"

    response = requests.get(f'{base_url}/users/9', data={"first_name": first_name, "last_name": last_name})
    body = response.json()

    assert response.json()["data"]["first_name"] == first_name
    assert response.status_code == 200
    schema = load_schema("list_of_users.json")
    with open(schema) as file:
        schema = json.load(file)
    validate(body, schema=schema)
    assert body["data"]["last_name"] == last_name


def test_user_update(base_url):
    name = "morpheus"
    job = "president"

    response = requests.patch(f"{base_url}/users/2", data={"name": name, "job": job})
    body = response.json()

    assert response.json()["name"] == name
    assert response.status_code == 200

    schema = load_schema("update_user.json")
    with open(schema) as file:
        schema = json.load(file)
    validate(body, schema=schema)
    assert body["job"] == job


def test_user_registration_not_success(base_url):
    response = requests.post(f"{base_url}//api/register", data={"email": "sydney@fife"})

    assert response.status_code == 404


def test_user_login_not_success(base_url):
    response = requests.post(f"{base_url}/login", data={"email": "peter@klaven"})

    assert response.status_code == 400
