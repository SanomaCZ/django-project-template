"""
Project settings are separated to
base.py  - basic application specific settings
local.py - settings specific to an installation (this should never be saved in repository)
"""
import sys

from {{ project_name }} import __versionstr__
from {{ project_name }}.settings.base import *

SERVER_CONFIGURATION_DIR = '/usr/local/etc/sanoma/'
sys.path.insert(0, SERVER_CONFIGURATION_DIR)

try:
    from {{ project_name }}_conf import *
except ImportError:
    pass
finally:
    del sys.path[0]

# finally local settings overides all
# overrides anything
try:
    from {{ project_name }}.settings.local import *
except ImportError:
    pass

#append version to STATIC_URL to invalidate old statics
STATIC_URL = '%sv%s/' % (STATIC_URL, __versionstr__)

# try to bump cache version by project version to avoid memcache reload
try:
    CACHES['default']['VERSION'] = __versionstr__
except KeyError:
    pass
