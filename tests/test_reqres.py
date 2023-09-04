import requests
from jsonschema.validators import validate
from conftest import load_json_schema, reqres_api


def test_users_status_code():
    response = reqres_api('get', '/api/users')

    assert response.status_code == 200


def test_users_per_page():
    per_page = 6

    response = reqres_api(
        'get',
        url='/api/users',
        params={'per_page': per_page}
    )

    assert response.json()['per_page'] == per_page
    assert len(response.json()['data']) == per_page


def test_users_schema():
    schema = load_json_schema('get_users_schema.json')

    response = reqres_api('get', '/api/users')
    validate(instance=response.json(), schema=schema)


def test_users_not_found():
    response = reqres_api('get', '/api/users/23')

    assert response.status_code == 404


def test_users_list_schema():
    schema = load_json_schema('get_users_list_schema.json')

    response = reqres_api('get', '/api/users')
    validate(instance=response.json(), schema=schema)


def test_create_users():
    response = reqres_api(
        'post',
        url='/api/users',
        data={'name': 'morpheus', 'job': 'leader'}
    )

    assert response.status_code == requests.codes.created
    assert response.json()['name'] == 'morpheus'
    assert response.json()['job'] == 'leader'


def test_update_users():
    response = reqres_api(
        'put',
        url='/api/users/2',
        data={'name': 'Anna', 'job': 'QA Automation Engineer'}
    )

    assert response.status_code == 200
    assert response.json()['name'] == 'Anna'
    assert response.json()['job'] == 'QA Automation Engineer'


def test_delete_users():
    response = requests.delete('https://reqres.in/api/users/2')
    # response = reqres_api('delete', '/api/users/2')

    assert response.status_code == 204


def test_register_successful():
    response = reqres_api(
        'post',
        url='/api/register',
        data={'email': 'eve.holt@reqres.in', 'password': 'pistol'}
    )

    assert response.status_code == 200
    assert response.json()['id'] == 4
    assert response.json()['token'] == 'QpwL5tke4Pnpja7X4'


def test_register_unsuccessful():
    response = reqres_api(
        'post',
        url='/api/register',
        data={'email': 'sydney@fife'}
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'


def test_login_successful():
    response = reqres_api(
        'post',
        url='/api/login',
        data={'email': 'eve.holt@reqres.in', 'password': 'cityslicka'}
    )

    assert response.status_code == 200
    assert response.json()['token'] == 'QpwL5tke4Pnpja7X4'


def test_login_unsuccessful():
    response = reqres_api(
        'post',
        url='/api/login',
        data={'email': 'peter@klaven'}
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'


def test_login_unsuccessful_unknown_user():
    response = reqres_api(
        'post',
        url='/api/login',
        data={'email': 'gdfsjgvld', 'password': '1234'}
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'user not found'


def test_login_unsuccessful_without_password():
    response = reqres_api(
        'post',
        url='/api/login',
        data={'email': 'eve.holt@reqres.in', 'password': ''}
    )

    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'
