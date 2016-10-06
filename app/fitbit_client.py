import base64
from contextlib import contextmanager

import fitbit
import requests

from app.models import save_fitbit_token
from config import get_current_config

# These grant permissions for your app to access user data.
# Ask for as little as possible
# Details https://dev.fitbit.com/docs/oauth2/
SCOPES = [
    'profile',
#    'activity',
#    'heartrate',
#    'location',
#    'nutrition',
#    'settings',
#    'sleep',
#    'social',
#    'weight'
]


@contextmanager
def fitbit_client(fitbit_credentials):
    config = get_current_config()
    client = fitbit.Fitbit(
        config.FITBIT_CLIENT_ID,
        config.FITBIT_CLIENT_SECRET,
        access_token=fitbit_credentials.access_token,
        refresh_token=fitbit_credentials.refresh_token
    )
    yield client
    # Save in case we did some refreshes
    save_fitbit_token(
        fitbit_credentials.user_id,
        client.client.token['access_token'],
        client.client.token['refresh_token']
    )


def get_permission_screen_url():
    return ('https://fitbit.com/oauth2/authorize'
            '?response_type=code&client_id={client_id}&scope={scope}').format(
        client_id=get_current_config().FITBIT_CLIENT_ID,
        scope='%20'.join(SCOPES)
    )


def get_token():
    config = get_current_config()
    return base64.b64encode(
        "{}:{}".format(
            config.FITBIT_CLIENT_ID,
            config.FITBIT_CLIENT_SECRET
        ).encode('utf-8')
    ).decode('utf-8')


def get_auth_url(code):
    return 'https://api.fitbit.com/oauth2/token?code={code}&client_id={client_id}&grant_type=authorization_code'.format(
        code=code,
        client_id=get_current_config().FITBIT_CLIENT_ID
    )


def do_fitbit_auth(code, user):
    r = requests.post(
        get_auth_url(code),
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic {}'.format(get_token()),
        }
    )
    r.raise_for_status()
    response = r.json()
    return save_fitbit_token(
        user.id,
        response['access_token'],
        response['refresh_token']
    )
