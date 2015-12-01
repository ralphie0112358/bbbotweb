import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

MOTOR1 = "P8_10"
MOTOR2 = "P8_12"
ENABLE = "P9_14"
PWM_HZ = 7800

def setup():
    GPIO.setup(MOTOR1, GPIO.OUT)
    GPIO.setup(MOTOR2, GPIO.OUT)
    GPIO.output(MOTOR1, GPIO.LOW)
    GPIO.output(MOTOR2, GPIO.LOW)

def cleanup():
    PWM.cleanup()
    GPIO.cleanup()

def stop(duty_cycle=90):
    PWM.start(ENABLE, duty_cycle, PWM_HZ)
    GPIO.output(MOTOR1, GPIO.HIGH)
    GPIO.output(MOTOR2, GPIO.HIGH)

def cw(duty_cycle=80):
    stop()
    PWM.start(ENABLE, duty_cycle, PWM_HZ)
    GPIO.output(MOTOR1, GPIO.LOW)
    GPIO.output(MOTOR2, GPIO.HIGH)

def ccw(duty_cycle=80):
    stop()
    PWM.start(ENABLE, duty_cycle, PWM_HZ)
    GPIO.output(MOTOR1, GPIO.HIGH)
    GPIO.output(MOTOR2, GPIO.LOW)


if __name__ == '__main__':
    import time
    setup()
    cw()
    time.sleep(2)
    stop()
    time.sleep(.5)
    ccw()
    time.sleep(2)
    stop()
    time.sleep(.5)
    cleanup()
