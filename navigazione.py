from motori import avanti, indietro, stop, chiudi
from sonar import misura_distanza, media_distanze
import time
import RPi.GPIO as GPIO

PULSANTE_AVVIO = 25
LED = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(PULSANTE_AVVIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

stato_attivo = False

try:
    
    while True:
        
        time.sleep(1)    
        print("Premi il pulsante per iniziare...")
        
        while GPIO.input(PULSANTE_AVVIO) == 1:
            GPIO.output(LED, GPIO.HIGH)
            time.sleep(0.1)
        
        print("Avvio...")
        stato_attivo = True
            
        while stato_attivo == True:
            
            dist = misura_distanza()
            speed = 6 * dist - 150             
            
            if speed > 0:
                if speed > 100:
                    speed =  100
                avanti(speed)
            
            elif speed < 0:
                if speed < -100:
                    speed = -100
                indietro(abs(speed))
            
            else:
                stop()

            print(speed)
            GPIO.output(LED, not GPIO.input(LED))
            
            time.sleep(0.1)
            
            if GPIO.input(PULSANTE_AVVIO) == 0:
                stop()
                time.sleep(0.2)
                stato_attivo = False
        
except KeyboardInterrupt:
    chiudi()
    
