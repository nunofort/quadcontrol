
#solenero.tech@gmail.com
#solenerotech.wordpress.com

#solenerotech 2013.09.06

from Motor import Motor
#import curses
import sys, select, tty, termios
import time

class NonBlockingConsole(object):
    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_data(self):
        try:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                return sys.stdin.read(1)
        except:
            return '[CTRL-C]'
        return False


#mymotor = motor('m1', 17, simulation=False)
#where 17 is  GPIO17 = pin 11
#mymotor = Motor('m1', 18)
#mymotor = Motor('m1', 23)
mymotor = Motor('m1', 24)
#mymotor = Motor('m1', 26)

#screen = curses.initscr()
#screen.clear()

print('***Disconnect ESC power')
print('***then press ENTER')
res = raw_input()
mymotor.start()
# set at maximum?
mymotor.setRPM(100)

#NOTE:the angular motor speed W can vary from 0 (min) to 100 (max)
#the scaling to pwm is done inside motor class
print('***Connect ESC Power')
print('***Wait beep-beep')

print('***then press ENTER')
res = raw_input()
# set at minimum?
mymotor.setRPM(0)
print('***Wait N beep for battery cell')
print('***Wait beeeeeep for ready')
print('***then press ENTER')
res = raw_input()
print ('increase > a | decrease > z | save Wh > n | set Wh > h|quit > q')

# turn off input echoing
#curses.noecho()
# respond to keys immediately (don't wait for enter)
#curses.cbreak()
# map arrow keys to special values
#screen.keypad(True)
cycling = True
try:
  with NonBlockingConsole() as nbc:
    while cycling:
        c = nbc.get_data()
        #c = raw_input()
        #c = screen.getch()
        if c == 'a':
            mymotor.increaseRPM()
        if c == 'z':
            mymotor.decreaseRPM()
        if c == 'q':
            cycling = False

except KeyboardInterrupt:
        pass

finally:
    # shut down cleanly
    #curses.nocbreak()
    #screen.keypad(0)
    #curses.echo()
    #curses.endwin()

    mymotor.stop()
    #mymotor.setRPM(0)
    print ("well done!")




