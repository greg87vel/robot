import RPi.GPIO as GPIO
import time


PIN_1 = 13
PIN_2 = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup([PIN_1, PIN_2], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def rilevamento_luce():
    return GPIO.input(PIN_1), GPIO.input(PIN_2)


if __name__ == '__main__':
    
    try:
        
        while True:
            
            print(rilevamento_luce())
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        GPIO.cleanup()
