import responses

from app.fitbit_client import get_token, get_auth_url, do_fitbit_auth
from app.models import get_user_fitbit_credentials


def test_get_token(test_client):
    assert get_token() == 'ZmFrZV9pZDpmYWtlX3NlY3JldA=='


@responses.activate
def test_do_fitbit_auth_saves_token(batman_user):
    code = 'code'
    responses.add(
        responses.POST,
        get_auth_url(code),
        json={'access_token': 'acc', 'refresh_token': 'ref'},
        match_querystring=True
    )

    creds = get_user_fitbit_credentials(batman_user.id)
    assert not creds
    do_fitbit_auth(code, batman_user)
    creds = get_user_fitbit_credentials(batman_user.id)
    assert creds.refresh_token == 'ref'
    assert creds.access_token == 'acc'
