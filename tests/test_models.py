import pytest

from app.models import User, get_user_fitbit_credentials, save_fitbit_token


def test_assert_password_not_accessible():
    user = User('test', 'test')
    with pytest.raises(AttributeError):
        user.password


def test_password_hashed():
    user = User('test', 'password')
    assert not user.password_hash == 'password'
    assert len(user.password_hash) > 8


def test_login():
    user = User('test', 'password')
    assert not user.validate('asdjasdaad')
    assert not user.validate('passwor')
    assert user.validate('password')


def test_save_fitbit_credentials(batman_user):
    creds = get_user_fitbit_credentials(batman_user.id)
    assert not creds
    save_fitbit_token(batman_user.id, 'acc', 'ref')
    creds = get_user_fitbit_credentials(batman_user.id)
    assert creds.refresh_token == 'ref'
    assert creds.access_token == 'acc'

