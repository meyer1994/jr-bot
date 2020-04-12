import os
from contextlib import contextmanager


@contextmanager
def resource(filename, *args, **kwargs):
    """ Open a resource from the resources directory """
    filename = os.path.join('tests/resources/', filename)
    with open(filename, *args, **kwargs) as file:
        yield file
