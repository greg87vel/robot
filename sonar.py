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
    distance_list = []  
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
    partial_dist = (elapsed_time * 34300) / 2  
    return int(partial_dist)


def media_distanze():   
    distance_list = []
    for _ in range(10):
        distance_list.append(misura_distanza())
        time.sleep(0.1)
    # Velocità del suono: 34300 cm/s (diviso per 2 per il tragitto andata/ritorno)
    distance = round(statistics.mean(distance_list), 2)
    return round(distance, 2)


if __name__ == "__main__":

    try:
        while True:
#             dist = media_distanze()
            dist = misura_distanza()
            print(f"Distanza: {dist} cm")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nInterrotto dall'utente. Pulizia dei GPIO...")
        GPIO.cleanup()
