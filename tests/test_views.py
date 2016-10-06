import responses
from fitbit.exceptions import BadResponse

from app.fitbit_client import get_auth_url
from app.models import save_fitbit_token, User


def register_batman(test_client):
    return test_client.post(
        '/register',
        data=dict(
            username='batman',
            password='robin',
            confirm='robin'
        ),
        follow_redirects=True
    )


def login_batman(test_client):
    return test_client.post(
        '/login',
        data=dict(
            username='batman',
            password='robin'
        ),
        follow_redirects=True
    )


def test_unauthed_index(test_client):
    response = test_client.get('/')
    assert b'login' in response.data


def test_unsuccessful_login(test_client):
    response = register_batman(test_client)
    assert response.status_code == 200
    response = test_client.post(
        '/login',
        data=dict(
            username='batman',
            password='joker'
        ),
        follow_redirects=True
    )
    assert response.status_code == 401
    assert b'Invalid Credentials' in response.data
    response = test_client.post(
        '/login',
        data=dict(
            username='joker',
            password='robin'
        ),
        follow_redirects=True
    )
    assert b'Invalid Credentials' in response.data
    assert response.status_code == 401


def test_logout(test_client):
    response = register_batman(test_client)
    assert response.status_code == 200
    response = login_batman(test_client)
    assert response.status_code == 200
    assert b'batman' in response.data
    response = test_client.get('/logout', follow_redirects=True)
    assert b'Logged Out' in response.data
    assert b'login' in response.data  # Redirected to login


def test_register_and_login_new_user(test_client):
    response = register_batman(test_client)
    assert response.status_code == 200
    response = login_batman(test_client)
    assert response.status_code == 200
    assert b'batman' in response.data


def test_reregistering_is_error(test_client):
    response = register_batman(test_client)
    assert response.status_code == 200
    response = register_batman(test_client)
    assert response.status_code == 400
    assert b'Username batman already taken' in response.data


@responses.activate
def test_handle_redirect(test_client):
    code = 'iamacode'

    # First we will do the authorization with the code
    # sent
    responses.add(
        responses.POST,
        get_auth_url(code),
        json={'access_token': 'acc', 'refresh_token': 'ref'},
        match_querystring=True
    )

    # Then we will get a token
    responses.add(
        responses.POST,
        'https://api.fitbit.com/oauth2/token',
        json={'access_token': 'acc', 'refresh_token': 'ref'}

    )

    # After getting the token we redirect to index which requests the profile
    responses.add(
        responses.GET,
        'https://api.fitbit.com/1/user/-/profile.json',
        json={'user': {'fullName': 'bat man', 'memberSince': '12/12/12'}}

    )

    register_batman(test_client)
    login_batman(test_client)
    response = test_client.get(
        '/oauth-redirect?code={}'.format(code),
        follow_redirects=True
    )

    assert b'batman' in response.data
    assert b'bat man' in response.data
    assert b'12/12/12' in response.data


@responses.activate
def test_api_call_failed(test_client):
    register_batman(test_client)
    save_fitbit_token(User.query.filter_by(username='batman').first().id, 'acc', 'ref')
    # Then we will get a token
    responses.add(
        responses.POST,
        'https://api.fitbit.com/oauth2/token',
        json={'access_token': 'acc', 'refresh_token': 'ref'}

    )

    # After getting the token we redirect to index which requests the profile
    responses.add(
        responses.GET,
        'https://api.fitbit.com/1/user/-/profile.json',
        body=BadResponse("I FAILED")

    )

    response = login_batman(test_client)
    assert b'Api Call Failed' in response.data
