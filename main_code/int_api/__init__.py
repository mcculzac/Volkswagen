import platform
if 'windows' not in platform.system().lower():
    raise ModuleNotFoundError('Invalid OS! Only runs on Windows at this time!')

from .email import *
from .generic import *
from .spreadsheet import *
from .file_manipulation import *
from .screen import *

__version__ = '1.0.0'
