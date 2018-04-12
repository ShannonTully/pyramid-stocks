import os
import pytest
from pyramid import testing
from ..models.meta import Base
from ..models import Stock, Account


@pytest.fixture
def test_stock():
    return Stock(
        companyName='fake',
        symbol='fake',
    )


@pytest.fixture
def configuration(request):
    """Setup a database for testing purposes."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://shannon:password@localhost:5432/testdata'
        # 'sqlalchemy.url': os.environ['TEST_DATABASE_URL']
    })
    config.include('pyramid_stocks.models')
    config.include('pyramid_stocks.routes')

    config.testing_securitypolicy(
        userid="user",
        permissive=True,
    )

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a database session for interacting with the test database."""
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Create a dummy GET request with a dbsession."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def test_account():
    return Account(username='user', email='user@user.com', password='password')
