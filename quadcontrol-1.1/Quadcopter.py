#    Quadcopter Main Interface           
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


from __future__ import print_function

from time import sleep
from time import time
from datetime import datetime
import logging
#from RPIO import PWM
from Motor import Motor

from Sensor import Sensor


class Quadcopter(object):

    __name = ''
    __version = 1
    __motor = [Motor(i, 0) for i in xrange(4)]
    __throttle = 0
    __throttlemin = 0 
    __throttlemax = 100
    __roll = 0
    __rollmin = -5
    __rollmax = 5
    __pitch = 0
    __pitchmin = -5
    __pitchmax = 5
    __yaw = 0
    __yawmin = -5
    __yawmax = 5
    __initenable = 0

    __debug = True
    #__logfile = 'quadcontrol.log'
    __logfp = False
    __log = logging.getLogger('Quadcopter_Class')


    def __init__(self, name, pin0=0,pin1=0,pin2=0,pin3=0, debug=True):
        self.__name = name
        self.__debug=debug

        self.__motor[0] = Motor(0, pin0, 1000, 0, 100, self.__debug)
        self.__motor[1] = Motor(1, pin1, 1000, 0, 100, self.__debug)
        self.__motor[2] = Motor(2, pin2, 1000, 0, 100, self.__debug)
        self.__motor[3] = Motor(3, pin3, 1000, 0, 100, self.__debug)

    #####################################################
    def sensorStart(self,enable,calib):
        imuLog = False
	calibIMU = calib
        if enable is True:
	   sim = False
	else:
	   sim = True
        self.__sensor = Sensor(imulog=imuLog, simulation=sim)

	if calibIMU:
    		self.__sensor.calibrate()
	self.__sensor.start()

    def sensorStop(self):
	self.__sensor.stop()
    #####################################################

    def setLogFile(self,logfp):
	self.__logfp=logfp
        for i in xrange(4):
	   self.__motor[i].setLogFile(self.__logfp)

    def setDebug(self,debug=True):
	self.__debug=debug

    def setPin(self,motor,pin, debug=True):
    	self.__motor[motor].setPin(pin)
	self.__motor[motor].setDebug(debug)

    def setKv(self,motor,kv=1000):
	self.__motor[motor].setKv(kv)

    def setRPMMin(self,motor,rpmmin=0):
        self.__motor[motor].setRPMMin(rpmmin)

    def getRPMMin(self,motor):
        return self.__motor[motor].getRPMMin()

    def setRPMMax(self,motor,rpmmax=100):
        self.__motor[motor].setRPMMax(rpmmax)

    def getRPMMax(self,motor):
        return self.__motor[motor].getRPMMax()

    def setRPM(self,motor,rpm=0):
	if self.__logfp != False:
		# testing???
		self.__logfp.write("MOTOR["+str(motor)+"] RPM: "+str(rpm)+"\n")
        self.__motor[motor].setRPM(rpm)

    def setRPMThrust(self,motor,rpm=50):
    	self.__motor[motor].setRPMThrust(rpm)
	
    def getRPM(self,motor):
        return self.__motor[motor].getRPM()

    def setInitEnable(self,bool):
	self.__initenable = bool

    def start(self):
        "start motors at minimum speed"
        for i in xrange(4):
            self.__motor[i].setRPM (0)

    def stop(self):
        self.sensorStop()
        "stop all motors"

	#STOP motors smoothly
        cycling=True
        self.__motor[0].decreaseRPM(10)
        rpm = self.__motor[0].getRPM()-10
        # SYNC motors
        self.__motor[1].setRPM(rpm+self.__motor[1].getRPMSYNC()) 
        self.__motor[2].setRPM(rpm+self.__motor[2].getRPMSYNC()) 
        self.__motor[3].setRPM(rpm+self.__motor[3].getRPMSYNC()) 
        while cycling is True:
          for i in xrange(4):
	    # DECREASE RPM
	    if self.__motor[i].getRPM() > 10:
               self.__motor[i].decreaseRPM(10)
          if self.__motor[0].getRPM() <= 10:
	     cycling = False  
        #STOP!
        for i in xrange(4):
            self.__motor[i].stop()
        self.__log.info(self.__name +' stopped')

    def startMotors(self):
       if self.__initenable == 1:
         for i in xrange(4):
            self.__logfp.write(str(datetime.today())+' QUADCOPTER: INIT MOTOR['+str(i)+']...\n')
            self.__motor[i].start()

    def startMotor(self,motor):
        if self.__initenable == 1:
          self.__logfp.write(str(datetime.today())+' QUADCOPTER: INIT MOTOR['+str(motor)+']...\n')
          self.__motor[motor].start()
          self.__motor[motor].log()

    def stopMotor(self,motor):
        self.__motor[motor].stop()
        #cycling=True
        #while cycling is True:
	#  if self.__motor[motor].getRPM() > 0:
        #    self.__motor[motor].decreaseRPM()
        #  else:
	#    cycling = False

    def increaseRPM(self,motor):
        self.__motor[motor].increaseRPM()

    def decreaseRPM(self,motor):
        self.__motor[motor].decreaseRPM()

    def setRPMEquil(self):
        "set RPMEquil all motors"
        for i in xrange(4):
            self.__motor[i].setRPMEquil()


    #hover
    def RPMEquil(self):
        "set RPM=RPMEquil all motors"
        for i in xrange(4):
            self.__motor[i].setRPM(self.__motor[i].getRPMEquil())

    def setMRPMSYNC(self,m,sync):
	self.__motor[m].setRPMSYNC(sync)
        self.__logfp.write("MOTOR["+str(m)+"] RPMSync: "+str(sync)+"\n")
	 
	# Calculate Sync RPM for motors from M1
    def setRPMSYNC(self):
        self.__logfp.write(str(datetime.today())+' QUADCOPTER: SYNC MOTORS RPM...\n')
        for i in xrange(4):
           self.__motor[i].log()
	   self.__motor[i].setRPMSYNC(0)

	for i in xrange(1,4):
	   #if self.__motor[i].getRPM() > self.__motor[0].getRPM():
	   #  self.__motor[i].setRPMSYNC(self.__motor[i].getRPM()-self.__motor[0].getRPM())
	   #if self.__motor[i].getRPM() < self.__motor[0].getRPM():
	   self.__motor[i].setRPMSYNC(self.__motor[i].getRPM()-self.__motor[0].getRPM())
           self.__logfp.write("MOTOR["+str(i)+"] RPMSync: "+str(self.__motor[i].getRPMSYNC())+"\n")

	self.__roll = 0
	self.__pitch = 0
	self.__yaw = 0
		
 
    # Syncronize Motors
    def syncRPM(self):
        #val=self.__motor[0].getRPM()
        #for i in xrange(4):
        for i in xrange(1,4):
	    self.__motor[i].syncRPM(self.__motor[0].getRPM())
            #if self.__motor[i].getRPM() != val: 
            #   self.__motor[i].setRPM(val)
      
    def getReady(self):
       #self.startMotors()
       for i in xrange(4):
           self.__motor[i].increaseRPM()
           self.__motor[i].decreaseRPM()
        
    ##########################################################################

    def moveUP(self):
        #Throttle
        #self.syncRPM()
	self.increaseThrottle()
        
    def moveDOWN(self):
        #Throttle
        #self.syncRPM()
	self.decreaseThrottle()

    def moveFORWARD(self):
	#self.increasePitch()
	self.increaseRoll()

    def moveBACKWARD(self):
	#self.decreasePitch()
	self.decreaseRoll()

    def turnLEFT(self):
        self.decreaseYaw()
        #self.setRPMSYNC()

    def turnRIGHT(self):
        self.increaseYaw()
        #self.setRPMSYNC()

    ##########################################################################
    def setThrottleMin(self,throttle):
	self.__throttleMin=throttle

    def setThrottleMax(self,throttle):
	self.__throttleMax=throttle

    def setRollMin(self,roll):
	self.echo('set roll : '+str(roll))
	self.__rollMin=roll

    def setRollMax(self,roll):
	self.__rollMax=roll

    def setPitchMin(self,pitch):
	self.__pitchMin=pitch

    def setPitchMax(self,pitch):
	self.__pitchMax=pitch

    def setYawMin(self,yaw):
	self.__yawMin=yaw

    def setYawMax(self,yaw):
	self.__yawMax=yaw

    def increaseThrottle(self):
	if self.__throttle < self.__throttleMax:
           for i in xrange(4):
              self.__motor[i].increaseRPM()
	   self.__throttle = self.__throttle+1

    def decreaseThrottle(self):
	if self.__throttle > self.__throttleMin:
           for i in xrange(4):
              self.__motor[i].decreaseRPM()
	   self.__throttle = self.__throttle-1

    def increaseRoll(self):
	if self.__roll < self.__rollMax:
           self.__motor[0].decreaseRPM()
           #self.motor[1].increaseRPM()
           self.__motor[2].increaseRPM()
           #self.motor[3].increaseRPM()
	   self.__roll = self.__roll+1

    def decreaseRoll(self):
	if self.__roll > self.__rollMin:
           self.__motor[0].increaseRPM()
           #self.motor[1].decreaseRPM()
           self.__motor[2].decreaseRPM()
           #self.motor[3].decreaseRPM()
	   self.__roll = self.__roll-1

    def increasePitch(self):
	if self.__pitch < self.__pitchMax:
           #self.motor[0].decreaseRPM()
           self.__motor[1].decreaseRPM()
           #self.motor[2].decreaseRPM()
           self.__motor[3].increaseRPM()
	   self.__pitch = self.__pitch+1

    def decreasePitch(self):
	if self.__pitch > self.__pitchMin:
           #self.motor[0].increaseRPM()
           self.__motor[1].increaseRPM()
           #self.motor[2].increaseRPM()
           self.__motor[3].decreaseRPM()
	   self.__pitch = self.__pitch-1

    def increaseYaw(self):
	if self.__yaw < self.__yawMax:
           self.__motor[0].increaseRPM()
           self.__motor[1].decreaseRPM()
           self.__motor[2].increaseRPM()
           self.__motor[3].decreaseRPM()
	   self.__yaw = self.__yaw+1

    def decreaseYaw(self):
	if self.__yaw > self.__yawMin:
           self.__motor[0].decreaseRPM()
           self.__motor[1].increaseRPM()
           self.__motor[2].decreaseRPM()
           self.__motor[3].increaseRPM()
	   self.__yaw = self.__yaw-1

    ###############################################

    def imuRoll(self):
	return self.__sensor.roll

    def imuPitch(self):
	return self.__sensor.pitch

    def imuYaw(self):
	return self.__sensor.yaw

    def accelRoll(self):
	return self.__sensor.roll_a

    def accelPitch(self):
	return self.__sensor.pitch_a

    def accelYaw(self):
	return self.__sensor.yaw_a

    def gyroRoll(self):
	return self.__sensor.roll_g

    def gyroPitch(self):
	return self.__sensor.pitch_g

    def gyroYaw(self):
	return self.__sensor.yaw_g

    ################################################

    def echo(self,text):
        if self.__debug == True:
           print (text)


    def log(self):
        try:
            #with open(self.__logfile, 'a+t') as log_file:
            #with open(self.__logfile, 'ab+') as log_file:
                #log_file.write(text+'\n')
                self.__logfp.write(str(datetime.today())+" QUADCOPTER: SAVING MOTORS INFORMATION...\n")
                for i in xrange(4):
                   self.__motor[i].log()

        except IOError, err:
            self.__log.critical('Error %d, %s accessing file', err.errno, err.strerror)

