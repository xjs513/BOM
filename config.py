#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from datetime import timedelta
# import logging
import logging.config

reload(sys)
sys.setdefaultencoding("utf-8")


SECRET_KEY = "DIALECT, DRIVER, USERNAM"
#PERMANENT_SESSION_LIFETIME = timedelta(days=7)
SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)


# dev
DEBUG = True
PORT = 5000
DB_FILE_PATH = 'C:\\code\\bom.mdb'


# logging.config.fileConfig("logger.conf")
# file_info_logger = logging.getLogger("file_info")
# file_error_logger = logging.getLogger("file_error")
# console_logger = logging.getLogger("root")
