from .model import FlyingWing
from .solver import WingSolver

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
