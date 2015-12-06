import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

import sys

MOTOR1A = "P8_10"
MOTOR1B = "P8_12"
ENCODER_AR = "P8_15"
ENCODER_AF = "P8_16"
ENCODER_BR = "P8_17"
ENCODER_BF = "P8_18"
ENABLE = "P9_14"
PWM_HZ = 7800


class Motor(object):
    def __init__(self):
        self.pos = 0
        self.dir = 'UNKNOWN'
        self.prev = 'UNKNOWN'

    def setup(self):
        GPIO.setup(MOTOR1A, GPIO.OUT)
        GPIO.setup(MOTOR1B, GPIO.OUT)
        GPIO.output(MOTOR1A, GPIO.LOW)
        GPIO.output(MOTOR1B, GPIO.LOW)
        GPIO.setup(ENCODER_AR, GPIO.IN)
        GPIO.setup(ENCODER_AF, GPIO.IN)
        GPIO.setup(ENCODER_BR, GPIO.IN)
        GPIO.setup(ENCODER_BF, GPIO.IN)
        GPIO.add_event_detect(ENCODER_AR, GPIO.RISING, Edger(self, 'AR'))
        GPIO.add_event_detect(ENCODER_AF, GPIO.FALLING, Edger(self, 'AF'))
        GPIO.add_event_detect(ENCODER_BR, GPIO.RISING, Edger(self, 'BR'))
        GPIO.add_event_detect(ENCODER_BF, GPIO.FALLING, Edger(self, 'BF'))

    def cleanup(self):
        PWM.cleanup()
        GPIO.cleanup()
    
    def stop(self, duty_cycle=90):
        PWM.start(ENABLE, duty_cycle, PWM_HZ)
        GPIO.output(MOTOR1A, GPIO.HIGH)
        GPIO.output(MOTOR1B, GPIO.HIGH)
    
    def cw(self, duty_cycle=80):
        self.stop()
        PWM.start(ENABLE, duty_cycle, PWM_HZ)
        GPIO.output(MOTOR1A, GPIO.LOW)
        GPIO.output(MOTOR1B, GPIO.HIGH)
    
    def ccw(self, duty_cycle=80):
        self.stop()
        PWM.start(ENABLE, duty_cycle, PWM_HZ)
        GPIO.output(MOTOR1A, GPIO.HIGH)
        GPIO.output(MOTOR1B, GPIO.LOW)

    def encoder_cb(self, detector):
        before = (self.prev, self.dir, self.pos)
        self._encoder_cb(detector)
        after = (self.prev, self.dir, self.pos)
        sys.stdout.write('%s ->%s\n' % (before, after))
        return 
        sys.stdout.write('\b\b\b\b\b\b\b\b')
        sys.stdout.write('{:8.2f}'.format(self.pos))
        sys.stdout.flush()
        
    def _encoder_cb(self, detector):
        if self.prev == 'UNKNOWN':
            self.prev = detector
            return
       
        if ((self.prev == 'AR' and detector == 'BR') or 
            (self.prev == 'AF' and detector == 'BF')):
            next_dir = 'FWD'

        elif ((self.prev == 'BR' and detector == 'AR') or 
            (self.prev == 'BF' and detector == 'AF')):
            next_dir = 'REV'

        elif ((self.prev == 'AR' and detector == 'AF') or
            (self.prev == 'AF' and detector == 'AR') or
            (self.prev == 'BR' and detector == 'BF') or
            (self.prev == 'BF' and detector == 'BR')):
            if self.dir == 'UNKNOWN':
                print 'huh'
            next_dir = 'REV' if self.dir == 'FWD' else 'FWD'

        else:
            next_dir = self.dir

        if next_dir == self.dir:
            if next_dir == 'FWD':
                self.pos += 0.5
            else:
                self.pos -= 0.5

        if next_dir != self.dir:
            if self.dir == 'UNKNOWN':
                if next_dir == 'FWD':
                    self.pos += 0.5
                else:
                    self.pos -= 0.5
        
        self.dir = next_dir
        self.prev = detector


class Edger(object):
    def __init__(self, motor, detector):
        self.motor = motor
        self.detector = detector

    def __call__(self, *args, **kwargs):
        self.motor.encoder_cb(self.detector)


if __name__ == '__main__':
    motor = Motor()
    motor.setup()
    import time
    motor.cw()
    time.sleep(2)
    motor.stop()
    time.sleep(.5)
    motor.ccw()
    time.sleep(2)
    motor.stop()
    time.sleep(.5)

    motor.cleanup()
