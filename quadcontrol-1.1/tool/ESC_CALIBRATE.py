
from Motor import Motor

motor1 = Motor(0, 18)
motor2 = Motor(1, 23)
motor3 = Motor(2, 24)
motor4 = Motor(3, 25)

motors = [motor1, motor2, motor3, motor4]

print('***Disconnect ESC power')
print('***then press ENTER')
res = raw_input()
try:
        for mitour in motors:
                mitour.start()
                mitour.setW(100)

	print('***Connect ESC Power')
	print('***Wait beep-beep')

        res = raw_input()
	for mitour in motors:
                mitour.start()
                mitour.setW(0)
	print('***Wait N beep for battery cell')
	print('***Wait beeeeeep for ready')
	print('***then press ENTER')
	res = raw_input()
	
	for mitour in motors:
                mitour.start()
                mitour.setW(10)
	res = raw_input()
finally:
    # shut down cleanly
        for mitour in motors:
                mitour.stop()

        print ("well done!")
        exit()


