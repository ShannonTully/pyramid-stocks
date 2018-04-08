from pyramid.response import Response
from pyramid.view import view_config
from ..sample_data import MOCK_DATA
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
import requests

from sqlalchemy.exc import DBAPIError

from ..models import MyModel

API_URL = 'https://api.iextrading.com/1.0'


# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def my_view(request):
#     try:
#         query = request.dbsession.query(MyModel)
#         one = query.filter(MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)
#     return {'one': one, 'project': 'pyramid_stocks'}


@view_config(route_name='home', renderer='../templates/index.jinja2', request_method='GET')
def get_home_view(request):
    return Response('Home')


@view_config(route_name='auth', renderer='../templates/auth.jinja2')
def get_auth_view(request):
    if request.method == 'GET':
        try:
            username = request.GET['username']
            password = request.GET['password']
            print('User: {}, Pass: {}'.format(username, password))

            return HTTPFound(location=request.route_url('portfolio'))

        except KeyError:
            return {}

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        print('User: {}, Pass: {}, Email: {}'.format(username, password, email))

        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()


@view_config(route_name='stock', renderer='../templates/stock-add.jinja2', request_method='GET')
def get_stock_view(request):
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}

        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        data = response.json()
        return {'company': data}

    else:
        raise HTTPNotFound()


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2', request_method='GET')
def get_portfolio_view(request):
    return {'data': MOCK_DATA}


@view_config(route_name='portfolio_symbol', renderer='../templates/stock-detail.jinja2', request_method='GET')
def get_portfolio_symbol_view(request):
    symbol = request.matchdict['symbol']

    for data in MOCK_DATA:
        if data['symbol'] == symbol:
            return {'data': data}
    return symbol


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyramid_stocks_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
