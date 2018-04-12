# Default view properties


def test_default_response_home_view(dummy_request):
    from ..views.default import get_home_view

    response = get_home_view(dummy_request)
    assert len(response) == 0
    assert type(response) == dict


# Auth View Functionality
def test_default_response_auth_view(dummy_request):
    from ..views.auth import auth_view

    response = auth_view(dummy_request)
    assert response == {}


def test_auth_signin_view(dummy_request):
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.GET = {'username': 'watman', 'password': 'whodat'}
    response = auth_view(dummy_request)
    assert response.status_code == 401


def test_auth_signup_view(dummy_request):
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'username': 'watman', 'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'POST'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_bad_reqeust_auth_signup_view(dummy_request):
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPBadRequest

    dummy_request.POST = {'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'POST'
    response = auth_view(dummy_request)
    assert response.status_code == 400
    assert isinstance(response, HTTPBadRequest)


def test_bad_request_method_auth_signup_view(dummy_request):
    from ..views.auth import auth_view
    from pyramid.httpexceptions import HTTPFound

    dummy_request.POST = {'password': 'whodat', 'email': 'wat@wat.com'}
    dummy_request.method = 'PUT'
    response = auth_view(dummy_request)
    assert response.status_code == 302
    assert isinstance(response, HTTPFound)


def test_default_notfound(dummy_request):
    from ..views.notfound import notfound_view

    assert notfound_view(dummy_request) == {}


def test_default_logout(dummy_request):
    from ..views.auth import logout
    from pyramid.httpexceptions import HTTPFound

    response = logout(dummy_request)
    assert isinstance(response, HTTPFound)