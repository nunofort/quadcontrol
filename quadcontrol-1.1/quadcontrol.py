
from time import sleep,time
import curses
import logging

from Motor import Motor
from Quadcopter import Quadcopter
from RControl import RControl

logger = logging.getLogger('Main Program')


control=RControl(debug=True)
#exit()
try:
  control.run()

except ImportError, strerror:
  logger.error('Error: Main Program, %s',strerror)

finally:
  #control.stop()
  print("DONE")

