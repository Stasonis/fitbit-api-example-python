from pytest import fixture

from app.models import User
from config import config
from app import create_app, db


@fixture
def test_client(flask_app):
    yield flask_app.test_client()


@fixture
def flask_app(monkeypatch):
    monkeypatch.setenv('FLASK_CONFIG', 'testing')
    f_app = create_app(config['testing'])
    db.create_all()
    yield f_app
    db.session.close()
    db.drop_all()


@fixture
def batman_user(flask_app):
    user = User('batman', 'bruce')
    db.session.add(user)
    db.session.commit()
    return user
