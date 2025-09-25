import RPi.GPIO as GPIO
import time

IR_DAVANTI_SX = 6
IR_DAVANTI_DX = 5                                  

GPIO.setmode(GPIO.BCM)
GPIO.setup([IR_DAVANTI_SX, IR_DAVANTI_DX], GPIO.IN)


def stato_ir_davanti_sx():
    return GPIO.input(IR_DAVANTI_SX)

def stato_ir_davanti_dx():
    return GPIO.input(IR_DAVANTI_DX)

if __name__ == "__main__":
    
    try:
    
        while True:
            
            print()
            print("IR DAVANTI SINISTRA: ", stato_ir_davanti_sx())
            print("IR DAVANTI DESTRA: ", stato_ir_davanti_dx())
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        GPIO.cleanup()
