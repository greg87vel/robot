import time
import RPi.GPIO as GPIO
import board
import busio
import adafruit_vl53l1x
import adafruit_vl53l0x

# --- Configurazioni ---
SHDN_PINS = {
    "frontale": 22,           # VL53L1X
    "laterale_dx_ant": 17,    # VL53L0X
}
NEW_ADDRESSES = {
    "laterale_dx_ant": 0x30,
}
DEFAULT_ADDRESS = 0x29

# --- Inizializzazione ---
i2c = busio.I2C(board.SCL, board.SDA)

GPIO.setmode(GPIO.BCM)
for pin in SHDN_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
time.sleep(0.1)

# --- Funzioni di supporto ---
def sensor_on(label):
    GPIO.output(SHDN_PINS[label], GPIO.HIGH)
    time.sleep(0.2)

def sensor_off(label):
    GPIO.output(SHDN_PINS[label], GPIO.LOW)
    time.sleep(0.01)

def scan_i2c():
    try:
        devices = i2c.scan()
        print("Dispositivi I2C rilevati:", [hex(addr) for addr in devices])
    except Exception as e:
        print("Errore durante la scansione I2C:", e)

# --- Spegni tutti ---
for label in SHDN_PINS:
    sensor_off(label)
time.sleep(0.2)

# --- Inizializza VL53L0X uno alla volta ---
from adafruit_vl53l0x import VL53L0X
vl53l0x_sensors = {}

for label, new_addr in NEW_ADDRESSES.items():
    print(f"\nInizializzazione {label} (VL53L0X)")
    for l in SHDN_PINS:
        sensor_off(l)
    time.sleep(0.2)

    sensor_on(label)
    scan_i2c()  # Debug I2C

    try:
        sensor = VL53L0X(i2c)
        sensor.set_address(new_addr)
        print(f"Indirizzo cambiato da 0x29 a {hex(new_addr)} per {label}")
        vl53l0x_sensors[label] = VL53L0X(i2c, address=new_addr)
    except Exception as e:
        print(f"Errore inizializzazione {label}: {e}")
    time.sleep(0.1)

# --- Inizializza VL53L1X frontale ---
print("\nInizializzazione frontale (VL53L1X)")
for l in SHDN_PINS:
    if l != "frontale":
        sensor_off(l)
time.sleep(0.2)

sensor_on("frontale")
scan_i2c()  # Debug I2C

try:
    vl53l1x = adafruit_vl53l1x.VL53L1X(i2c)
    vl53l1x.distance_mode = 1
    vl53l1x.timing_budget = 200
    vl53l1x.start_ranging()
    print("Sensore frontale inizializzato.")
except Exception as e:
    print(f"Errore inizializzazione VL53L1X frontale: {e}")
    vl53l1x = None

# --- Funzione lettura ---
def leggi_distanze():
    distanze = {
        "frontale": None,
        "laterale_dx_ant": None,
        "laterale_dx_post": None
    }

    try:
        if vl53l1x and vl53l1x.data_ready:
            distanze["frontale"] = vl53l1x.distance
            vl53l1x.clear_interrupt()
    except Exception as e:
        print(f"Errore lettura VL53L1X: {e}")

    for label, sensor in vl53l0x_sensors.items():
        try:
            distanze[label] = sensor.range
        except Exception as e:
            print(f"Errore lettura {label}: {e}")

    return distanze

# --- Ciclo principale ---
if __name__ == '__main__':
    try:
        while True:
            d = leggi_distanze()
            print("----")
            print(f'   Frontale: {d["frontale"]} mm')
            print(f'   DX Ant:   {d["laterale_dx_ant"]} mm')
            print(f'   DX Post:  {d["laterale_dx_post"]} mm')
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Interrotto manualmente.")
    finally:
        GPIO.cleanup()
