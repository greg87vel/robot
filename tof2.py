import time
import board
import busio
import RPi.GPIO as GPIO
import adafruit_vl53l0x

# --- CONFIGURAZIONE ---
# Cambia questo valore per testare un sensore diverso
SHDN_PIN = 13 # GPIO collegato al pin SHDN del sensore da testare

# --- INIZIALIZZAZIONE GPIO ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(SHDN_PIN, GPIO.OUT)
GPIO.output(SHDN_PIN, GPIO.LOW)
time.sleep(0.1)  # tempo per spegnere il sensore

# Accendi il sensore
GPIO.output(SHDN_PIN, GPIO.HIGH)
time.sleep(0.2)  # tempo per stabilizzarsi

# --- INIZIALIZZAZIONE I2C ---
i2c = busio.I2C(board.SCL, board.SDA)

# --- TEST DEL SENSORE ---
try:
    sensor = adafruit_vl53l0x.VL53L0X(i2c)
    print("✅ Sensore rilevato correttamente.")
    print("Leggo la distanza ogni 0.5 secondi. Premi CTRL+C per uscire.\n")
    while True:
        print(f"Distanza: {sensor.range} mm")
        time.sleep(0.5)

except Exception as e:
    print("❌ Errore nel rilevare il sensore. Verifica cablaggio e SHDN.")
    print(f"Dettagli: {e}")

finally:
    GPIO.cleanup()
