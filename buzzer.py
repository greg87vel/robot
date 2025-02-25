import RPi.GPIO as GPIO
import time

BUZZER = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

def suona_buzzer(n):
    for i in range(n):
        GPIO.output(BUZZER, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(BUZZER, GPIO.LOW)
        time.sleep(0.2)
    
if __name__ == "__main__":
    
    try:
        while True:
            GPIO.output(BUZZER, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(BUZZER, GPIO.LOW)
            time.sleep(0.2)
    except KeyboardInterrupt:
        GPIO.cleanup()
