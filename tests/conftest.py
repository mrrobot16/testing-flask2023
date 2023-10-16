import pytest
from app import create_app

@pytest.fixture
def app():
    """Create a Flask app context for the tests."""
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def sample_fixture():
    print("Setting up the fixture...")
    yield
    print("Tearing down the fixture...")

