"""
try behave
"""
import os
import git

import semantic_version
__author__ = 'Mike Carifio <mike@carif.io>'

here = os.path.dirname(__file__)
version = '0.0.1'
version_suffix = git.get_current_tag(here, git.get_current_branch(here))
if version_suffix:
    __version__ = semantic_version.Version(version + '+git' + version_suffix)
else:
    __version__ = semantic_version.Version(version)


import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('{levelname}:{pathname}:{lineno} | {message}', style='{')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.debug('why does format matter?')

if '__main__' == __name__:
    logger.debug('start main')
