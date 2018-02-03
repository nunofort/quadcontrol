#    Quadcopter Web Control Interface
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

#2015.03.14
#################################################################################

import threading
import logging
import time
import sys
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import re

from Motor import Motor
from Quadcopter import Quadcopter
from RControl import RControl


class Webserver(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.server = HTTPServer(('quadcontrol', 80), MyHandler)
        self.logger = logging.getLogger('Quadcontrol')

        MyHandler.logger = logging.getLogger('Quadcontrol.H')
	MyHandler.control = RControl(debug=True)
        MyHandler.webaccess = False
	MyHandler.webhost = '' 

        try:
            f = open(curdir + sep + '/www/index.html')
            MyHandler.mypage = f.read()
            f.close()
            MyHandler.logger.debug(MyHandler.mypage)
        except IOError, err:
            self.logger.critical('Error %d, %s accessing file: %s', err.errno, err.strerror, 'myQ.html')


    def run(self):
        try:
            self.logger.debug('Webserver running...')
            self.server.serve_forever()

	except KeyboardInterrupt:
	    print('^C received, shutting down server')
	    self.server.socket.close()

        except:
            self.logger.critical('Unexpected error:', sys.exc_info()[0])

    def stop(self):
        self.server.socket.close()
        self.logger.debug('Webserver stopped')



class MyHandler(BaseHTTPRequestHandler):


    def do_cmd(self,cmd):
        try:
	    print ("COMMAND: %s" % cmd)
   	    self.control.cmd(cmd)
	    #rpm_m1=self.control.getRPM(0)

            self.send_response(200)
            self.send_header('Content-type', 'text/html;charset=utf-8')
	    #r="<h1>Hello World</h1>"
	    #self.send_header("Content-length", len(r))
	    #self.send_header("Access-Control-Allow-Origin","*")
            self.end_headers()
            #self.wfile.write(self.mypage)
            #self.wfile.write(r.encode("utf-8"))
            #self.wfile.write(bytes(r,"utf-8"))
            s1=''
            s2=''
            s3=''
	    # mpu6050 enabled?
            if self.control.mpu6050():
               s1 = ' IMU | roll: ' + str(self.control.imuRoll())
               s1 += ' | pitch: ' + str(self.control.imuPitch())
               s1 += ' | yaw: ' + str(self.control.imuYaw())
            
               s2 = 'ACCEL | roll: ' + str(self.control.accelRoll())
               s2 += ' | pitch: ' + str(self.control.accelPitch())
               s2 += ' | yaw: ' + str(self.control.accelYaw())
            
               s3 = 'GYRO | roll: ' + str(self.control.gyroRoll())
               s3 += ' | pitch: ' + str(self.control.gyroPitch())
               s3 += ' | yaw: ' + str(self.control.gyroYaw())

            s = """\
<!--
The local time of this server is:  %s <br>
The timezone of this server is  :  %s <br>
<br>
-->
CMD: %s<br>
<br>
<table>
<tr>
<td>
[M1] [0-100] RPM: %u &nbsp;&nbsp;
</td>
<td>
%s
</td>
</tr>
<tr>
<td>
[M2] [0-100] RPM: %u &nbsp;&nbsp;
</td>
<td>
%s
</td>
</tr>
<tr>
<td>
[M3] [0-100] RPM: %u &nbsp;&nbsp;
</td>
<td>
%s
</td>
</tr>
<tr>
<td colspan=2>
[M4] [0-100] RPM: %u
</td>
</tr>
</table>

""" % (
time.ctime(time.time()), time.timezone/3600,
cmd,
self.control.getRPM(0),
s1,
self.control.getRPM(1),
s2,
self.control.getRPM(2),
s3,
self.control.getRPM(3))


	    self.wfile.write(s.encode("utf-8"))
            #self.wfile.write('[M1] [0-100] RPM: 1')
            #self.wfile.write('<br/>[M2] [0-100] RPM: 1')
            #self.wfile.write('<br/>[M3] [0-100] RPM: 1')
            #self.wfile.write('<br/>[M4] [0-100] RPM: 1')
            #self.wfile.write('<br/>CMD: ' + cmd)
            #self.wfile.write('<p>')
	    #self.wfile.flush()
	    #self.wfile.close()

        except:
            self.logger.critical('Unexpected error')

    def do_GET(self):
        
	if self.path=="/":
		self.path="/index.html"
        try:

	    sendReply = False
	    #if self.path.endswith("cmd.py?cmd=UP"):
	    #	mimetype='text/html'
	    #   sendReply = True
	    if self.path.endswith(".html"):
		mimetype='text/html'
		sendReply = True
	    if self.path.endswith(".jpg"):
		mimetype='image/jpg'
		sendReply = True
	    if self.path.endswith(".gif"):
		mimetype='image/gif'
		sendReply = True
	    if self.path.endswith(".js"):
		mimetype='application/javascript'
		sendReply = True
	    if self.path.endswith(".css"):
		mimetype='text/css'
		sendReply = True

            m = re.search(r'\?pass=([a-zA-Z0-9]+)',self.path)
            if m is not None:
                print m.group()
                print "STR1: "+m.group(1)
                print "STR1: "+self.control.webpass()
                if self.control.webpass() == '':
		   MyHandler.webaccess = True
		else:
		   if m.group(1) == self.control.webpass():
		      MyHandler.webaccess = True
		#print "!"+str(MyHandler.webaccess)
		if MyHandler.webaccess:
		   #self.webhost = str(self.client_address.port)
		   print "HOST: "+self.webhost
		   mimetype='text/html'
		   sendReply = True
		   self.path="/index.html"
          
	    print "ACCESS: "+str(MyHandler.webaccess)

            #m = re.search(r'\?pass=([a-zA-Z0-9]+)&cmd=([A-Z0-9]+)',self.path)
            m = re.search(r'\?cmd=([A-Z0-9]+)',self.path)
            if m is not None:
                print m.group()
                print "STR1: "+m.group(1)
                #print "STR2: "+m.group(2)
                if MyHandler.webaccess:
		   self.do_cmd(m.group(1))
		#print m.group()[5:]
		#self.do_cmd(m.group()[5:])

	    """
            if self.path.endswith("?cmd=UP"):
	    self.do_cmd('UP')
	    """
	    
            if MyHandler.webaccess:
	      if sendReply == True:
		try:
		   #Open the static file requested and send it
		   f = open(curdir + sep + '/www'+ self.path) 
		   self.send_response(200)
		   self.send_header('Content-type',mimetype)
		   self.end_headers()
		   self.wfile.write(f.read())
		   f.close()
	        except IOError:
		   self.send_error(404,'File Not Found: %s' % self.path)
	    return

        except:
            self.logger.critical('Unexpected error')





