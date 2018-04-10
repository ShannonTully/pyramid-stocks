from pyramid.response import Response
from pyramid.view import view_config
from ..sample_data import MOCK_DATA
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPBadRequest
from pyramid.security import NO_PERMISSION_REQUIRED
import requests

from sqlalchemy.exc import DBAPIError, IntegrityError

from ..models import Stock
from ..models import Account

API_URL = 'https://api.iextrading.com/1.0'


# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def my_view(request):
#     try:
#         query = request.dbsession.query(MyModel)
#         one = query.filter(MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)
#     return {'one': one, 'project': 'pyramid_stocks'}


@view_config(route_name='home', renderer='../templates/index.jinja2', request_method='GET', permission=NO_PERMISSION_REQUIRED)
def get_home_view(request):
    # return Response('Home')
    return {}


# @view_config(route_name='auth', renderer='../templates/auth.jinja2')
# def get_auth_view(request):
#     if request.method == 'GET':
#         try:
#             username = request.GET['username']
#             password = request.GET['password']
#             print('User: {}, Pass: {}'.format(username, password))

#             return HTTPFound(location=request.route_url('portfolio'))

#         except KeyError:
#             return {}

#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         print('User: {}, Pass: {}, Email: {}'.format(username, password, email))

#         return HTTPFound(location=request.route_url('portfolio'))

#     return HTTPNotFound()


@view_config(route_name='stock', renderer='../templates/stock-add.jinja2')
def get_stock_view(request):
    if request.method == 'GET':
        try:
            symbol = request.GET['symbol']
        except KeyError:
            return {}

        response = requests.get(API_URL + '/stock/{}/company'.format(symbol))
        data = response.json()
        return {'data': data}

    # else:
    #     raise HTTPNotFound()

    if request.method == 'POST':
        if not all([field in request.POST for field in ['companyName', 'symbol', 'exchange', 'website', 'ceo', 'industry', 'sector', 'issueType', 'description']]):
            raise HTTPBadRequest
        # import pdb; pdb.set_trace()
        new = Stock()
        new.companyName = request.POST['companyName']
        new.symbol = request.POST['symbol']
        new.exchange = request.POST['exchange']
        new.website = request.POST['website']
        new.CEO = request.POST['ceo']
        new.industry = request.POST['industry']
        new.sector = request.POST['sector']
        new.issueType = request.POST['issueType']
        new.description = request.POST['description']

        try:
            request.dbsession.add(new)
            request.dbsession.flush()
        except IntegrityError:
            pass

        return HTTPFound(location=request.route_url('portfolio'))

    return HTTPNotFound()


@view_config(route_name='portfolio', renderer='../templates/portfolio.jinja2', request_method='GET')
def get_portfolio_view(request):
    query = request.dbsession.query(Stock)
    return {'data': query.all()}


@view_config(route_name='portfolio_symbol', renderer='../templates/stock-detail.jinja2', request_method='GET')
def get_portfolio_symbol_view(request):
    try:
        symbol = request.matchdict['symbol']
        query = request.dbsession.query(Stock)
        for data in query.all():
            if data.symbol == symbol:
                return {'data': data}
        return symbol
    except KeyError:
        return HTTPNotFound()