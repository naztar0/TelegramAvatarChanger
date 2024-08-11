import logging
import json
from contextvars import ContextVar


logging.basicConfig(level=logging.INFO)


CONFIG = ContextVar('config')

with open('config.json') as _f:
    CONFIG.set(json.load(_f))
