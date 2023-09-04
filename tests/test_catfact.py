from conftest import catfact_api


def test_get_breeds():
    response = catfact_api(
        'get',
        url='/breeds',
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) > 1


def test_get_cats_limit():
    limit = 6

    response = catfact_api(
        'get',
        url='/facts',
        params={'limit': limit}
    )

    assert len(response.json()["data"]) == limit


def test_get_cats_max_length():
    max_length = 40

    response = catfact_api(
        'get',
        url='/facts',
        params={'max_length': max_length}
    )

    assert all([len(fact) <= max_length for fact in response.json()["data"]])


def test_get_cats_max_length_and_quantit():
    limit = 6
    max_length = 35

    response = catfact_api(
        'get',
        url='/facts',
        params={'limit': limit, 'max_length': max_length}
    )

    assert len(response.json()["data"]) <= limit
    assert all([len(fact) <= max_length for fact in response.json()["data"]])
