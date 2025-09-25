import RPi.GPIO as GPIO
import time
import statistics

# Definizione dei pin
TRIG_PIN = 23
ECHO_PIN = 18

# Imposta i pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)


def misura_distanza():
    """Misura la distanza utilizzando l'HC-SR04."""    
    # Invia impulso al trigger
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001) 
    GPIO.output(TRIG_PIN, False)
    # Aspetta che il segnale venga ricevuto
    start_time = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()
    # Calcola la durata dell'eco
    elapsed_time = stop_time - start_time   
    dist = (elapsed_time * 34300) / 2  
    return int(dist)



if __name__ == "__main__":

    try:
        while True:
            dist = misura_distanza()
            print(f"Distanza: {dist} cm")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nInterrotto dall'utente. Pulizia dei GPIO...")
        GPIO.cleanup()
