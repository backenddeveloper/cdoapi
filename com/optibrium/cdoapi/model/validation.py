from com.optibrium.cdoapi.model import Animal
from com.optibrium.cdoapi.model import database
from com.optibrium.cdoapi.model import Security
from com.optibrium.cdoapi.model.exceptions import Forbidden
from com.optibrium.cdoapi.model.exceptions import Invalid
from com.optibrium.cdoapi.model.exceptions import NotFound
from flask import request
import re


def valid_authentication_required(func):

    def decorated(*args, **kwargs):

        if 'x-api-key' in request.headers:
            Security.check_token(request.headers['x-api-key'])

        elif 'token' in request.cookies.keys():
            Security.check_token(request.cookies['token'])

        else:
            raise Forbidden('Unauthorised')

        return func(*args, **kwargs)

    decorated.__name__ = func.__name__
    return decorated


def valid_name_required(func):

    def decorated(*args, **kwargs):

        data = request.get_json(force=True)

        if 'name' not in data:
            raise Invalid('Name not found')

        if re.findall('[^0-9a-zA-Z]', data['name']):
            raise Invalid('Names must be alphanumeric')

        return func(data['name'], *args, **kwargs)

    decorated.__name__ = func.__name__
    return decorated


def existent_species_required(func):

    def decorated(*args, **kwargs):

        if not database.session \
                       .query(Animal) \
                       .filter(Animal.species == kwargs['species']) \
                       .all():
            raise NotFound()

        return func(*args, **kwargs)

    decorated.__name__ = func.__name__
    return decorated
