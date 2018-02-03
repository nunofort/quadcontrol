
from time import sleep,time
import curses
import logging

#from Motor import Motor
#from Quadcopter import Quadcopter
#from RControl import RControl

from Webserver import Webserver

logger = logging.getLogger('Main Program')


try:
  webserver = Webserver()
  webserver.run()
  #exit()

except ImportError, strerror:
  logger.error('Error: Main Program, %s',strerror)

finally:
  print("DONE")

