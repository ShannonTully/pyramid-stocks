# Default view properties
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from pyramid.security import remember



def test_default_response_portfolio_view(dummy_request):
    from ..views.default import get_portfolio_view

    response = get_portfolio_view(dummy_request)
    assert isinstance(response, HTTPNotFound)
    # assert response['data'] == []


def test_default_get_portfolio_symbol_view(dummy_request, db_session, test_stock, test_account):
    from ..views.default import get_portfolio_symbol_view

    test_stock.account_id.append(test_account)
    db_session.add(test_stock)
    db_session.add(test_account)

    # db_session.flush()

    dummy_request.matchdict = {'symbol': 'fake'}
    # remember(dummy_request, userid='user')
    # import pdb; pdb.set_trace()
    response = get_portfolio_symbol_view(dummy_request)
    assert type(response) == dict
    assert response['data'].symbol == 'fake'


def test_detail_not_found(dummy_request):
    from ..views.default import get_portfolio_symbol_view
    from pyramid.httpexceptions import HTTPNotFound

    response = get_portfolio_symbol_view(dummy_request)
    assert isinstance(response, HTTPNotFound)


def test_default_response_get_stock_view(dummy_request):
    from ..views.default import get_stock_view

    response = get_stock_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


def test_valid_post_to_get_stock_view(dummy_request, db_session, test_account):
    from ..views.default import get_stock_view
    from pyramid.httpexceptions import HTTPFound

    db_session.add(test_account)

    dummy_request.method = 'POST'
    dummy_request.POST = {
        "symbol": "sytest",
        "companyName": "cntest",
        "exchange": "extest",
        "industry": "intest",
        "website": "wstest",
        "description": "dctest",
        "ceo": "ceotest",
        "issueType": "istest",
        "sector": "sctest",
    }

    response = get_stock_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_valid_post_to_get_stock_view_adds_record_to_db(dummy_request, test_account, db_session):
    from ..views.default import get_stock_view
    from ..models import Stock

    db_session.add(test_account)

    dummy_request.method = 'POST'
    dummy_request.POST = {
        "symbol": "sytest",
        "companyName": "cntest",
        "exchange": "extest",
        "industry": "intest",
        "website": "wstest",
        "description": "dctest",
        "ceo": "ceotest",
        "issueType": "istest",
        "sector": "sctest",
    }

    # assert right here that there's nothing in the DB

    get_stock_view(dummy_request)
    query = db_session.query(Stock)
    one = query.first()
    assert one.companyName == 'cntest'
    assert one.symbol == 'sytest'
    assert type(one.id) == int


def test_invalid_post_to_get_stock_view(dummy_request):
    import pytest
    from ..views.default import get_stock_view
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.method = 'POST'
    dummy_request.POST = {}

    with pytest.raises(HTTPBadRequest):
        response = get_stock_view(dummy_request)
        assert isinstance(response, HTTPBadRequest)
