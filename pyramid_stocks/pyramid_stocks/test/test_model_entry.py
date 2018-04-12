from datetime import datetime


def test_constructed_stock_with_correct_date_added_to_database(db_session):
    from ..models import Stock

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        companyName='test 1',
        symbol='this is a test',
    )
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


def test_constructed_stock_with_no_date_added_to_database(db_session):
    from ..models import Stock

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        companyName='test 1',
        symbol='this is a test',
    )
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


def test_constructed_stock_with_date_added_to_database(db_session):
    from ..models import Stock

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        companyName='test 1',
        symbol='this is a test',
    )
    db_session.add(stock)
    assert len(db_session.query(Stock).all()) == 1


def test_stock_with_no_title_throws_error(db_session):
    from ..models import Stock
    import pytest
    from sqlalchemy.exc import IntegrityError

    assert len(db_session.query(Stock).all()) == 0
    stock = Stock(
        companyName='test 1',
    )
    with pytest.raises(IntegrityError):
        db_session.add(stock)

        assert db_session.query(Stock).one_or_none() is None
