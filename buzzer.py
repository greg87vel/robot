import RPi.GPIO as GPIO
import time

BUZZER = 5
LED = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup([BUZZER, LED], GPIO.OUT)
GPIO.output([BUZZER, LED], GPIO.LOW)

def suona_buzzer(n):
    for i in range(n):
        GPIO.output([BUZZER, LED], GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output([BUZZER, LED], GPIO.LOW)
        time.sleep(0.2)
    
if __name__ == "__main__":
    
    try:
        while True:
            GPIO.output([LED, BUZZER], GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output([LED, BUZZER], GPIO.LOW)
            time.sleep(0.2)
    except KeyboardInterrupt:
        GPIO.cleanup()
