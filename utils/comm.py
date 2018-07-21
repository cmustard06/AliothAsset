#!/usr/bin/env python
# __Author__:cmustard

"""
commom function
"""
import logging


from utils.config import LOGFILE,LOGLEVEL


LOGMAP = {"debug":logging.DEBUG,"warning":logging.WARNING,"warn":logging.WARN,"error":logging.ERROR}

def get_logger():
	'''generate logger'''
	logger = logging.Logger("asset")
	logger.setLevel(LOGMAP[LOGLEVEL.lower()])
	formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	                              datefmt='%a, %d %b %Y %H:%M:%S')
	file_handler = logging.FileHandler(LOGFILE)
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	return logger

if __name__ == '__main__':
    logger = get_logger()
    logger.warn("test!!!")
