import RPi.GPIO as GPIO
import time

# IMPORTANTE: COLLEGARE LA FOTORESISTENZA AI 3,3V, NON AI 5V!!!

FOTORES = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(FOTORES, GPIO.OUT)

def valore_fotoresistenza():
    return GPIO.input(FOTORES)


if __name__ == '__main__':
    
    while True:
        
        print(GPIO.input(FOTORES))
        time.sleep(0.5)
