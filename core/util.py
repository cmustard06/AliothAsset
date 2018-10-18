#!/usr/bin/env python
# __Author__:cmustard

import logging
from core.config import LOGPATH,LOGLEVEL



def logger():
	lo = logging.Logger("Alioth")
	lo.setLevel(LOGLEVEL)
	formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - log message: %(message)s",datefmt="%Y-%m-%d %A %H:%M:%S")
	filehandler = logging.FileHandler(LOGPATH)
	filehandler.setFormatter(formatter)
	lo.addHandler(filehandler)
	if LOGLEVEL==logging.DEBUG:
		shandler = logging.StreamHandler()
		shandler.setFormatter(formatter)
		lo.addHandler(shandler)
	return lo

