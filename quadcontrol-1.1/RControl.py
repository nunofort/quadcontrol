#    Quadcopter Remote Control Interface     
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
from time import sleep,time
from Quadcopter import Quadcopter
import logging
import curses

class RControl(object):
    __quadcop = object
    __keyINITM1 = '1'
    __keyINITM2 = '2'
    __keyINITM3 = '3'
    __keyINITM4 = '4'
    __keyINCM1 = 'x'
    __keyDECM1 = 'z'
    __keyINCM2 = 'v'
    __keyDECM2 = 'c'
    __keyINCM3 = 'n'
    __keyDECM3 = 'b'
    __keyINCM4 = ','
    __keyDECM4 = 'm'

    __keyUP = 'w'
    __keyDOWN = 's'
    __keyFORWARD = 'q'
    __keyBACKWARD = 'a'
    __keyRIGHT = 'o'
    __keyLEFT = 'i'
    __keySETEQUIL = 'e'
    __keyEQUIL = '0'
    __keySYNC = 'p'
    __keySTOP = chr(32)
    __keyQUIT = chr(32)

    __keyINCROLL = 'l'
    __keyDECROLL = 'k'
    __keyINCPITCH = 'j'
    __keyDECPITCH = 'h'
    __keyINCYAW = 'g'
    __keyDECYAW = 'f'

    __debug = True
    __logfile = 'quadcontrol.log' # THE BLACK BOX OF THE FLIGHT!
    __logfp=False
    __log = logging.getLogger('RemoteControl_Class')
    __webpass = ''
    __mpu6050 = False
    

    def __init__(self, debug=True):
	self.__debug = debug
	self.__quadcop = Quadcopter("quad", 18, 23, 24, 25, True)
	self.__quadcop.setDebug(debug);
	self.load('quadcontrol.cfg')

	#self.__quadcop.startMotors()
	#self.__quadcop.load('quadcontrol.cfg')
	#exit()
	self.__quadcop.getReady()

    def setLogFile(self,logfile):
        try:
	    self.__logfile=logfile
            self.__logfp=open(self.__logfile, 'a+t')
            #with open(self.__logfile, 'a+t') as log_file:
            #with open(self.__logfile, 'ab+') as log_file:
            #self.__logfp=log_file

        except IOError, err:
            self.__log.critical('Error %d, %s accessing file: %s', err.errno, err.strerror, self.__logfile)

        self.__quadcop.setLogFile(self.__logfp)

	
    def loadConfig(self,line):
        line = line[:-1]
        if len(line) > 0:
          if line[0] == '#':
                self.__log.debug('Loading comment %s ', line)
                print ("Loading comment")
          else:
                tok = line.split('=')
                if len(tok) == 2:
                        name=tok[0].strip()
                        value=tok[1].strip()
		        if name.startswith( 'key' ):
			  #if value.isdecimal():
			  if value.isdigit():
			    #value=str(unichr(int(value)))
			    value=chr(int(value))
			  if value.startswith(":") or value.startswith("'"):
			    value=value[1:2]
                        self.__log.debug('Loading %s = %s', tok[0],tok[1])
                        print ("LOADING CONFIG [%s] = [%s]" % (name, value))
                        if name == 'debug':
			     if value == 'true':
			       self.__debug = True
			     else:
			       self.__debug = False
                        if name == 'logfile':
			     self.setLogFile(value)
			     #self.__logfile = value
                        if name == 'webpass':
			     self.__webpass = value
                        if name == 'mpu6050':
			     if value == 'true':
			       self.__mpu6050 = True
			     else:
			       self.__mpu6050 = False
			     self.__quadcop.sensorStart(self.__mpu6050, calib=False)
			########################################
                        if name == 'M1':
                          self.__quadcop.setPin(0,int(value))
                        if name == 'M2':
                          self.__quadcop.setPin(1,int(value))
                        if name == 'M3':
                          self.__quadcop.setPin(2,int(value))
                        if name == 'M4':
                          self.__quadcop.setPin(3,int(value))
			########################################
                        if name == 'M1_KV':
                          self.__quadcop.setKv(0,int(value))
                        if name == 'M1_RPM':
                          self.__quadcop.setRPM(0,int(value))
                          self.__quadcop.setMRPMSYNC(0,int(value))
                        if name == 'M1_RPMMIN':
                          self.__quadcop.setRPMMin(0,int(value))
                        if name == 'M1_RPMMAX':
                          self.__quadcop.setRPMMax(0,int(value))
                        if name == 'M1_THRUST':
                          self.__quadcop.setRPMThrust(0,int(value))
                        if name == 'M2_KV':
                          self.__quadcop.setKv(1,int(value))
                        if name == 'M2_RPM':
                          self.__quadcop.setRPM(1,int(value))
                          self.__quadcop.setMRPMSYNC(1,int(value))
                        if name == 'M2_RPMMIN':
                          self.__quadcop.setRPMMin(1,int(value))
                        if name == 'M2_RPMMAX':
                          self.__quadcop.setRPMMax(1,int(value))
                        if name == 'M2_THRUST':
                          self.__quadcop.setRPMThrust(1,int(value))
                        if name == 'M3_KV':
                          self.__quadcop.setKv(2,int(value))
                        if name == 'M3_RPM':
                          self.__quadcop.setRPM(2,int(value))
                          self.__quadcop.setMRPMSYNC(2,int(value))
                        if name == 'M3_RPMMIN':
                          self.__quadcop.setRPMMin(2,int(value))
                        if name == 'M3_RPMMAX':
                          self.__quadcop.setRPMMax(2,int(value))
                        if name == 'M3_THRUST':
                          self.__quadcop.setRPMThrust(2,int(value))
                        if name == 'M4_KV':
                          self.__quadcop.setKv(3,int(value))
                        if name == 'M4_RPM':
                          self.__quadcop.setRPM(3,int(value))
                          self.__quadcop.setMRPMSYNC(3,int(value))
                        if name == 'M4_RPMMIN':
                          self.__quadcop.setRPMMin(3,int(value))
                        if name == 'M4_RPMMAX':
                          self.__quadcop.setRPMMax(3,int(value))
                        if name == 'M4_THRUST':
                          self.__quadcop.setRPMThrust(3,int(value))
			#########################################
		        #DONT NEED, USE M_RPM!
                        #if name == 'M1_RPMSYNC':
                        #  self.__quadcop.setMRPMSYNC(0,int(value))
                        #if name == 'M2_RPMSYNC':
                        #  self.__quadcop.setMRPMSYNC(1,int(value))
                        #if name == 'M3_RPMSYNC':
                        #  self.__quadcop.setMRPMSYNC(2,int(value))
                        #if name == 'M4_RPMSYNC':
                        #  self.__quadcop.setMRPMSYNC(3,int(value))
		        #########################################
                        if name == 'THROTTLE_MIN':
			  self.__quadcop.setThrottleMin(int(value))
                        if name == 'THROTTLE_MAX':
			  self.__quadcop.setThrottleMax(int(value))
                        if name == 'ROLL_MIN':
			  self.__quadcop.setRollMin(int(value))
                        if name == 'ROLL_MAX':
			  self.__quadcop.setRollMax(int(value))
                        if name == 'PITCH_MIN':
			  self.__quadcop.setPitchMin(int(value))
                        if name == 'PITCH_MAX':
			  self.__quadcop.setPitchMax(int(value))
                        if name == 'YAW_MIN':
			  self.__quadcop.setYawMin(int(value))
                        if name == 'YAW_MAX':
			  self.__quadcop.setYawMax(int(value))
			###########################################
                        if name == 'INITENABLE':
                          self.__quadcop.setInitEnable(int(value[0]))
                        if name == 'keyINITM1':
                          self.__keyINITM1 = value[0]
                        if name == 'keyINITM2':
                          self.__keyINITM2 = value[0]
                        if name == 'keyINITM3':
                          self.__keyINITM3 = value[0]
                        if name == 'keyINITM4':
                          self.__keyINITM4 = value[0]
                        if name == 'keyINCM1':
                          self.__keyINCM1 = value[0]
                        if name == 'keyDECM1':
                          self.__keyDECM1 = value[0]
                        if name == 'keyINCM2':
                          self.__keyINCM2 = value[0]
                        if name == 'keyDECM2':
                          self.__keyDECM2 = value[0]
                        if name == 'keyINCM3':
                          self.__keyINCM3 = value[0]
                        if name == 'keyDECM3':
                          self.__keyDECM3 = value[0]
                        if name == 'keyINCM4':
                          self.__keyINCM4 = value[0]
                        if name == 'keyDECM4':
                          self.__keyDECM4 = value[0]
                        ############################################
                        if name == 'keyUP':
                          self.__keyUP = value[0]
                        if name == 'keyDOWN':
                          self.__keyDOWN = value[0]
                        if name == 'keyFORWARD':
                          self.__keyFORWARD = value[0]
                        if name == 'keyBACKWARD':
                          self.__keyBACKWARD = value[0]
                        if name == 'keyRIGHT':
                          self.__keyRIGHT = value[0]
                        if name == 'keyLEFT':
                          self.__keyLEFT = value[0]
                        if name == 'keySETEQUIL':
                          self.__keySETEQUIL = value[0]
                        if name == 'keyEQUIL':
                          self.__keyEQUIL = value[0]
                        if name == 'keySYNC':
                          self.__keySYNC = value[0]
                        if name == 'keySTOP':
                          self.__keySTOP = value[0]
                        if name == 'keyINCROLL':
                          self.__keyINCROLL = value[0]
                        if name == 'keyDECROLL':
                          self.__keyDECROLL = value[0]
                        if name == 'keyINCPITCH':
                          self.__keyINCPITCH = value[0]
                        if name == 'keyDECPITCH':
                          self.__keyDECPITCH = value[0]
                        if name == 'keyINCYAW':
                          self.__keyINCYAW = value[0]
                        if name == 'keyDECYAW':
                          self.__keyDECYAW = value[0]
                else:
                        print ("UNDEFINED CONFIG LINE!")


    def load(self, file_name):
        try:
            with open(file_name, 'r') as cfg_file:
                while cfg_file.read(1) != '':
                  cfg_file.seek(-1,1)
                  print ("Loading config line...")
                  line = cfg_file.readline()
                  if len(line) > 0:
                    print (line)
                    self.loadConfig(line)
                    #ver = self.getInt(cfg_file)
                    #if ver is not self.__version:
                    #    self.__log.critical('cfg file not compatible: need version 1')
                    #self.ip = self.getIp(cfg_file)
                cfg_file.flush()
                #cfg_file.close()

        except IOError, err:
            self.__log.critical('Error %d, %s accessing file: %s', err.errno, err.strerror, file_name)

    
    def log(self):
        try:
            #with open(self.__logfile, 'a+t') as f:
            #with open(self.__logfile, 'ab+') as log_file:
                #log_file.write(text+'\n')
                #print ("QUADCOPTER: SAVING MOTORS INFORMATION...",file=f)

		self.__quadcop.log()

                #log_file.write('[1] RPM: '+str(self.__quadcop.getRPM(0))+'\n')
                #log_file.write('[2] RPM: '+str(self.__quadcop.getRPM(1))+'\n')
                #log_file.write('[3] RPM: '+str(self.__quadcop.getRPM(2))+'\n')
                #log_file.write('[4] RPM: '+str(self.__quadcop.getRPM(3))+'\n')
               
        except IOError, err:
            self.__log.critical('Error %d, %s accessing file: %s', err.errno, err.strerror, self.__logfile)

    # NOT USED!
    def saveQuadLog(self,text):
        try:
            with open(self.__logfile, 'a+t') as log_file:
            #with open(self.__logfile, 'ab+') as log_file:
                #log_file.write(text+'\n')
                print('QUADCOPTER: SAVING MOTORS INFORMATION...',log_file)
                log_file.write('[1] RPM: '+str(self.__quadcop.getRPM(0))+'\n')
                log_file.write('[2] RPM: '+str(self.__quadcop.getRPM(1))+'\n')
                log_file.write('[3] RPM: '+str(self.__quadcop.getRPM(2))+'\n')
                log_file.write('[4] RPM: '+str(self.__quadcop.getRPM(3))+'\n')
               
        except IOError, err:
            self.__log.critical('Error %d, %s accessing file: %s', err.errno, err.strerror, self.__logfile)

    def webpass(self):
	return self.__webpass

    def mpu6050(self):
	return self.__mpu6050

    def getRPMMin(self,m):
        return self.__quadcop.getRPMMin(m)

    def getRPMMax(self,m):
        return self.__quadcop.getRPMMax(m)

    def getRPM(self,m):
        return self.__quadcop.getRPM(m)

    ###############################################

    def imuRoll(self):
        return self.__quadcop.imuRoll()

    def imuPitch(self):
        return self.__quadcop.imuPitch()

    def imuYaw(self):
        return self.__quadcop.imuYaw()

    def accelRoll(self):
        return self.__quadcop.accelRoll()

    def accelPitch(self):
        return self.__quadcop.accelPitch()

    def accelYaw(self):
        return self.__quadcop.accelYaw()

    def gyroRoll(self):
        return self.__quadcop.gyroRoll()

    def gyroPitch(self):
        return self.__quadcop.gyroPitch()

    def gyroYaw(self):
        return self.__quadcop.gyroYaw()
    ################################################

    def cmd(self,cmd):
      	#For tuning
	######################################
      	if cmd == "INCM1":
       		self.__quadcop.increaseRPM(0)
      	if cmd == "DECM1":
       		self.__quadcop.decreaseRPM(0)
       	if cmd == "INCM2":
       		self.__quadcop.increaseRPM(1)
      	if cmd == "DECM2":
       		self.__quadcop.decreaseRPM(1)
      	if cmd == "INCM3":
       		self.__quadcop.increaseRPM(2)
      	if cmd == "DECM3":
       		self.__quadcop.decreaseRPM(2)
      	if cmd == "INCM4":
       		self.__quadcop.increaseRPM(3)
      	if cmd == "DECM4":
       		self.__quadcop.decreaseRPM(3)

       	#######################################
       	if cmd == "UP":
       		self.__quadcop.moveUP()
       	if cmd == "DOWN":
       		self.__quadcop.moveDOWN()
       	if cmd == "FORWARD":
       		self.__quadcop.moveFORWARD()
       	if cmd == "BACKWARD":
       		self.__quadcop.moveBACKWARD()
       	if cmd == "RIGHT":
       		self.__quadcop.turnRIGHT()
       	if cmd == "LEFT":
       		self.__quadcop.turnLEFT()
       	if cmd == "SETEQUIL":
       		self.__quadcop.setRPMEquil()
        if cmd == "EQUIL":
       		self.__quadcop.RPMEquil()
       	if cmd == "SYNC":
       		self.__quadcop.setRPMSYNC()
       	#######################################
        #if cmd == "INCTHR":
        #    self.__quadcop.increaseThrottle()
        #if cmd == "DECTHR":
        #    self.__quadcop.decreaseThrottle()
        if cmd == "INCROLL":
            self.__quadcop.increaseRoll()
        if cmd == "DECROLL":
            self.__quadcop.decreaseRoll()
        if cmd == "INCPITCH":
            self.__quadcop.increasePitch()
        if cmd == "DECPITCH":
            self.__quadcop.decreasePitch()
        if cmd == "INCYAW":
            self.__quadcop.increaseYaw()
        if cmd == "DECYAW":
            self.__quadcop.decreaseYaw()

        #Init Motor
       	#######################################
        if cmd == "INITM1":
        	self.__quadcop.startMotor(0)
        if cmd == "INITM2":
        	self.__quadcop.startMotor(1)
        if cmd == "INITM3":
        	self.__quadcop.startMotor(2)
        if cmd == "INITM4":
        	self.__quadcop.startMotor(3)
        if cmd == "STOP":
		self.stop()



    def run(self):
	LoopCycleTime = 0.1

	#logger = __logging.getLogger(__name__)
	screen = curses.initscr()

      	# turn off input echoing
  	curses.noecho()
	# respond to keys immediately (don't wait for enter)
	curses.cbreak()
	# map arrow keys to special values
	screen.keypad(True)
	res=0
	cycling = True
	cycletime = 0

	try:
    	   while cycling:
        	cyclestart = time()
        	screen.addstr(0,0,'SPACE for quit/STOP')
        	screen.addstr(1,10,'Startup motor procedure: 1-2-3-4 ')
        	screen.addstr(2,10,'9 to stop qpi')
        	screen.addstr(3,20,'Tune motors:a-z,s-x,d-c,f-v')
        	screen.addstr(4,20,'Tune motors: set RPMEquil e')
        	screen.addstr(5,30,'jog qpi: roll i-m ,pitch j-l, yaw u-o')
        	screen.addstr(6,30,'jog qpi: Throttle y-n ,hover h')

        	screen.addstr(18,2,'[1] ['+str(self.__quadcop.getRPMMin(0))+'-'+str(self.__quadcop.getRPMMax(0))+'] RPM: '+str(self.__quadcop.getRPM(0)))
        	screen.addstr(20,2,'[2] ['+str(self.__quadcop.getRPMMin(1))+'-'+str(self.__quadcop.getRPMMax(1))+'] RPM: '+str(self.__quadcop.getRPM(1)))
        	screen.addstr(22,2,'[3] ['+str(self.__quadcop.getRPMMin(2))+'-'+str(self.__quadcop.getRPMMax(2))+'] RPM: '+str(self.__quadcop.getRPM(2)))
        	screen.addstr(24,2,'[4] ['+str(self.__quadcop.getRPMMin(3))+'-'+str(self.__quadcop.getRPMMax(3))+'] RPM: '+str(self.__quadcop.getRPM(3)))

		if self.__mpu6050:
                  s = ' IMU |roll: ' + str(self.__quadcop.imuRoll())
                  s += '|pitch: ' + str(self.__quadcop.imuPitch())
                  s += '|yaw: ' + str(self.__quadcop.imuYaw())

                  s1 = 'ACCEL|roll: ' + str(self.__quadcop.accelRoll())
                  s1 += '|pitch: ' + str(self.__quadcop.accelPitch())
        	  s1 += '|yaw: ' + str(self.__quadcop.accelYaw())

        	  s2 = 'GYRO |roll: ' + str(self.__quadcop.gyroRoll())
        	  s2 += '|pitch: ' + str(self.__quadcop.gyroPitch())
        	  s2 += '|yaw: ' + str(self.__quadcop.gyroYaw())

        	  screen.addstr(18, 25, s)
        	  screen.addstr(20, 25, s1)
        	  screen.addstr(22, 25, s2)

        	screen.refresh()
        	screen.timeout(-1)

        	res = screen.getch()
        	screen.clear()
        	#screen.addstr(24,50,str(res))
        	cyclestart = time()
        	if res == -1:
            		self.__quadcop.stop()
        	#For tuning
		######################################
        	if res ==ord(self.__keyINCM1):
			self.cmd("INCM1")
        	if res == ord(self.__keyDECM1):
			self.cmd("DECM1")
        	if res == ord(self.__keyINCM2):
			self.cmd("INCM2")
        	if res == ord(self.__keyDECM2):
			self.cmd("DECM2")
        	if res == ord(self.__keyINCM3):
			self.cmd("INCM3")
        	if res == ord(self.__keyDECM3):
			self.cmd("DECM3")
        	if res == ord(self.__keyINCM4):
			self.cmd("INCM4")
        	if res == ord(self.__keyDECM4):
			self.cmd("DECM4")
        	#######################################
        	if res == ord(self.__keyUP):
			self.cmd("UP")
        	if res == ord(self.__keyDOWN):
			self.cmd("DOWN")
        	if res == ord(self.__keyFORWARD):
			self.cmd("FORWARD")
        	if res == ord(self.__keyBACKWARD):
			self.cmd("BACKWARD")
        	if res == ord(self.__keyRIGHT):
			self.cmd("RIGHT")
        	if res == ord(self.__keyLEFT):
			self.cmd("LEFT")
        	if res == ord(self.__keySETEQUIL):
			self.cmd("SETEQUIL")
        	if res == ord(self.__keyEQUIL):
			self.cmd("EQUIL")
        	if res == ord(self.__keySYNC):
			self.cmd("SYNC")
        	#######################################

        	#if res == ord('y'):
        	#    self.cmd("INCTHR")
        	#if res == ord('n'):
        	#    self.cmd("DECTHR")
        	if res == ord(self.__keyINCROLL):
        	    self.cmd("INCROLL")
        	if res == ord(self.__keyDECROLL):
        	    self.cmd("DECROLL")
        	if res == ord(self.__keyINCPITCH):
        	    self.cmd("INCPITCH")
        	if res == ord(self.__keyDECPITCH):
        	    self.cmd("DECPITCH")
        	if res == ord(self.__keyINCYAW):
            	    self.cmd("INCYAW")
        	if res == ord(self.__keyDECYAW):
            	    self.cmd("DECYAW")

        	#Init Motor
		########################################
        	if res == ord(self.__keyINITM1):
            		self.cmd("INITM1")
        	if res == ord(self.__keyINITM2):
            		self.cmd("INITM2")
        	if res == ord(self.__keyINITM3):
            		self.cmd("INITM3")
        	if res == ord(self.__keyINITM4):
            		self.cmd("INITM4")
        	if res == ord(self.__keySTOP):
            		self.cmd("STOP")
			cycling = False
		if res == 27: # ESC
            		self.cmd("STOP")
			cycling = False

        	#this is for not processing all the buffer,
        	#but a command per cycle
        	curses.flushinp()
        	cycleend = time()
        	cycletime =cycleend-cyclestart
        	if cycletime < LoopCycleTime:
            		sleep(LoopCycleTime-cycletime)
        	else:
            		self.__log.warning('Loop cycle time exceed '+ str(LoopCycleTime))

	finally:
    	   # shut down cleanly
    	   curses.nocbreak()
    	   screen.keypad(0)
    	   curses.echo()
    	   curses.endwin()


    def stop(self):
	self.log()
	self.__quadcop.stop()


    def echo(self,text):
	if self.__debug == True:
	   print (text)




