#    Quadcopter Motor Interface 
#
#    Copyright (C) 2015  Nuno Fortes
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
################################################################################

# (original work by solenero.tech@gmail.com, solenerotech.wordpress.com) 

# by Nuno Fortes
# nunofort@gmail.com
# fortbits.blogger.com
# http://sourceforge.net/users/nunofort/

#2015.02.22 
#################################################################################

from time import sleep
from datetime import datetime
import logging
from RPIO import PWM

class Motor(object):

    __id=0
    __pin=0
    __kv=0
    __RPM = 0      # given in %
    __RPMMin = 1    # given in %
    __RPMMax = 100    # given in %
    __RPMEquil = 50    # RPM that hibry the gravity,in%
    __RPMThrust = 50   # is the rpmequil
    __RPMSync = 0      # RPM Sync from prev motor
    __debug=True
    __logfp=False
    __log=logging.getLogger(__name__)

    def __init__(self, id, pin, kv=1000, rpmmin=1, rpmmax=100,debug=True ):
        self.__id = id
        self.__pin = pin
        self.__kv = kv
        self.setRPMLimits(rpmmin, rpmmax)
        self.__RPM = self.__RPMMin

        try:
            from RPIO import PWM
            self.__IO = PWM.Servo()
        except ImportError, strerror:
            self.__log.error('Error: Motor NOT initialized, %s',strerror)

    def setDebug(self, debug=True):
	self.__debug=debug

    def setLogFile(self,logfp):
	self.__logfp=logfp

    def setPin(self, pin):
        "set the pin for each motor"
        self.__pin = pin

    def setKv(self, kv):
        "set the kv for each motor"
        self.__kv = kv

    def setRPMMin(self, RPMMin):
        if RPMMin < 0:
            RPMMin = 0
        self.__RPMMin = RPMMin

    def getRPMMin(self):
	return self.__RPMMin
	
    def setRPMMax(self, RPMMax):
        if RPMMax > 100:
            RPMMax = 100
        self.__RPMMax = RPMMax
	
    def getRPMMax(self):
	return self.__RPMMax
	
    def setRPMLimits(self, RPMMin, RPMMax):
	self.setRPMMin(RPMMin)
	self.setRPMMax(RPMMax)

    def setRPMThrust(self, rpm):
	self.__RPMThrust = rpm
	self.__RPMEquil = rpm 

    def setRPMSYNC(self, sync):
	self.__RPMSync=sync

    def getRPMSYNC(self):
	return self.__RPMSync

    # Syncronize Motor
    def syncRPM(self,rpm):
	self.setRPM(rpm+self.__RPMSync)

    def setRPMEquil(self):
        "Sets current RPM% =RPMEquil"
        self.__RPMEquil = self.__RPM
        #logging.warning('M' + str(self.__mId) + ' RPM equiv %: ' + str(self.__RPMEquil))

    def getRPMEquil(self):
        "returns current RPM% =RPMEquil"
        return self.__RPMEquil

    def start(self):
        try:
          "Run the procedure to init the ESC"
          self.setRPM(0)

          #TODO verify this startup cycle
          self.__IO.set_servo(self.__pin, 2000)
          sleep(1)
          self.__IO.stop_servo(self.__pin)
          #self.setRPM(10)
          self.setRPM(0)

          self.__log.info('M' + str(self.__id) + ' started')
        except err:
	    self.log()
            self.__log.critical('Error %d, %s', err.errno, err.strerror)

    def stop(self):
        "Sets RPM=0"
        self.setRPM(0)

        self.__IO.stop_servo(self.__pin)

        self.__log.info('M' + str(self.__id) + ' stopped')

    def increaseRPM(self, step=1):
        "increases RPM% for the motor"
        self.__RPM = self.__RPM + step
        self.setRPM(self.__RPM)

    def decreaseRPM(self, step=1):
        "decreases RPM% for the motor"
        self.__RPM = self.__RPM - step
        self.setRPM(self.__RPM)

    def setRPM(self, RPM):
        "Checks RPM% is between limits than sets it"
        PW = 0
        try:
          self.__RPM = RPM
          if self.__RPM < self.__RPMMin:
            self.__RPM = 0
          if self.__RPM > self.__RPMMax:
            self.__RPM = self.__RPMThrust
          self.__log.debug('M' + str(self.__id) + ' RPM %: ' + str(self.__RPM))
          PW = (1000 + (self.__RPM) * 10)
          # Set servo to xxx us
          self.__log.debug('GPIO' + str(self.__pin) + ' PW: ' + str(PW))
          self.__IO.set_servo(self.__pin, PW)
          #if self.powered:
        except: 
          self.__IO.stop_servo(self.__pin)

    def getRPM(self):
        "retuns current RPM%"
        return self.__RPM

    def echo(self,text):
        if self.__debug == True:
           print (text)

    def print_some(self):
        print (self.__kv)


    def log(self):
        try:
          #logfp.write(text+'\n')
          #print('QUADCOPTER: SAVING MOTORS INFORMATION...',logfp)
          self.__logfp.write(str(datetime.today())+' MOTOR['+str(self.__id)+'] RPM: '+str(self.__RPM)+'\n')

        except IOError, err:
            self.__log.critical('Error %d, %s', err.errno, err.strerror)

