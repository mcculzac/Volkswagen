import platform
import os
if 'windows' not in platform.system().lower():
    raise ModuleNotFoundError('Invalid OS! Only runs on Windows at this time!')

from .email import *
from .generic import *
from .spreadsheet import *
from .file_manipulation import *
from .screen import *
from .model_utils import *

__version__ = '1.0.0'
__main_code_path__ = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '\\data\\clean_data\\'
