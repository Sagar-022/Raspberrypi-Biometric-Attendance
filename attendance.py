import RPi.GPIO as GPIO
from pyfingerprint.pyfingerprint import PyFingerprint
import MySQLdb
import time
from pyfingerprint.pyfingerprint import PyFingerprint

db = MySQLdb.connect(host="localhost",
                     user="hannan",
                     passwd="tech",
                     db="attendance")
cur = db.cursor()

attendanceMode = False
current_class_no = 0

def readCurrentClassNo():
    global current_class_no
    cur.execute("select cc from current_class_no;")
    r = cur.fetchone()
    current_class_no = r[0]

def startNewClass():
    global current_class_no
    current_class_no = current_class_no + 1
    cur.execute("update current_class_no set cc = cc +1;")
    cur.execute("select roll from student;")
    for row in cur.fetchall():
        roll = row[0]
        cur.execute("insert into sheet values("+str(current_class_no)+","+str(roll)+",'Absent');")
    db.commit()

def makePresent(pos):
    if attendanceMode == False:
        print("mode is off but making present")
        turnOff()
    cur.execute("update sheet set attend='Present' where class_no="+str(current_class_no)+" and roll in (select roll from student where finger_pos = "+str(pos)+");")
    print("attendance registered for " + str(pos))
    db.commit()

def turnOff():
    print("exitting...")
    GPIO.cleanup()
    db.close()
    exit(0)

prevButtonState = True   #   not pushed - active low circuit
def checkAttendanceButton():
    global prevButtonState
    global attendanceMode
    newButtonState = GPIO.input(attendanceButton)
    if prevButtonState == True and newButtonState == False:
        attendanceMode = not attendanceMode
        print("button pushed")
        if attendanceMode == True:
            startNewClass()
    prevButtonState = newButtonState
    time.sleep(0.005)   # for contact bounce problem in push buttons

programLED = 37
attendanceLED = 35
foundLED = 33
notFoundLED = 31
attendanceButton = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(attendanceButton, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(notFoundLED, GPIO.OUT)
GPIO.setup(foundLED, GPIO.OUT)
GPIO.setup(attendanceLED, GPIO.OUT)
GPIO.setup(programLED, GPIO.OUT)

GPIO.output(programLED, True)
time.sleep(1)
GPIO.output(programLED, False)

programLEDPWM = GPIO.PWM(programLED, 0.4)
programLEDPWM.start(4)

GPIO.output(attendanceLED, False)
GPIO.output(foundLED, False)
GPIO.output(notFoundLED, False)

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    turnOff()

readCurrentClassNo()

try:
    while True:
        if attendanceMode == True:
            GPIO.output(attendanceLED, True)
            try:
                print('Waiting for finger...')
                while ( f.readImage() == False ):
                    checkAttendanceButton()
                    if attendanceMode == False:
                        break
                if attendanceMode == True:
                    f.convertImage(0x01)
                    result = f.searchTemplate()

                    positionNumber = result[0]

                    if ( positionNumber == -1 ):
                        print("no match found")
                        GPIO.output(notFoundLED, True)
                        time.sleep(1)
                        GPIO.output(notFoundLED, False)
                    else:
                        makePresent(positionNumber)
                        GPIO.output(foundLED, True)
                        time.sleep(1)
                        GPIO.output(foundLED, False)
            except Exception as e:
                print('Operation failed!')
                print('Exception message: ' + str(e))
                turnOff()

            
        elif attendanceMode == False:
            GPIO.output(attendanceLED, False)
        
        checkAttendanceButton()

    
except KeyboardInterrupt,  e:
    turnOff()
