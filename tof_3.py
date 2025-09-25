import time
import board
import busio
import smbus2
import RPi.GPIO as GPIO
import adafruit_vl6180x

# --- Configurazioni ---
I2C_BUS = 1
DEFAULT_ADDRESS = 0x29
NEW_ADDRESSES = [0x30, 0x31]
SHDN_PINS = [17, 27]  # GPIO per destra_davanti e destra_dietro

# --- Setup GPIO ---
GPIO.setmode(GPIO.BCM)
for pin in SHDN_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# --- Pausa lunga per garantire reset completo ---
print("Spegnimento completo dei sensori...")
time.sleep(1.0)

# --- Bus I2C per cambio indirizzo (smbus2) ---
bus = smbus2.SMBus(I2C_BUS)
i2c = busio.I2C(board.SCL, board.SDA)

# --- Funzione scrittura word a 16 bit ---
def write_word(addr, reg, val):
    data = [(reg >> 8) & 0xFF, reg & 0xFF, val]
    write = smbus2.i2c_msg.write(addr, data)
    bus.i2c_rdwr(write)

# --- Cambio indirizzo I2C ---
def change_address(old_addr, new_addr):
    print(f" → Cambio indirizzo {hex(old_addr)} → {hex(new_addr)}")
    write_word(old_addr, 0x0212, new_addr)
    time.sleep(0.1)

# --- Inizializzazione sensori ---
sensors = []
for i, new_addr in enumerate(NEW_ADDRESSES):
    print(f"\n--- Inizializzazione sensore {i} (GPIO {SHDN_PINS[i]}) ---")

    # Spegne entrambi
    for pin in SHDN_PINS:
        GPIO.output(pin, GPIO.LOW)
    time.sleep(0.5)

    # Accende solo quello corrente
    GPIO.output(SHDN_PINS[i], GPIO.HIGH)
    time.sleep(0.5)

    try:
        # Verifica se il sensore è vivo su 0x29
        print("Controllo presenza a 0x29...")
        model_id = bus.read_byte_data(DEFAULT_ADDRESS, 0x00)
        print(f" → Model ID: {hex(model_id)}")

        # Cambia indirizzo
        change_address(DEFAULT_ADDRESS, new_addr)

        # Crea istanza Adafruit
        sensor = adafruit_vl6180x.VL6180X(i2c, address=new_addr)
        sensors.append(sensor)
        print(f" → Sensore inizializzato a {hex(new_addr)}")

    except Exception as e:
        print(f"Errore durante setup del sensore {i}: {e}")

# --- Riaccende entrambi i sensori per l'uso continuo ---
for pin in SHDN_PINS:
    GPIO.output(pin, GPIO.HIGH)
time.sleep(0.1)

# --- Lettura ---
def leggi_distanze_doppie(n_misure=5):
    nomi = ['destra_davanti', 'destra_dietro']
    distanze = {}

    for nome, sensor in zip(nomi, sensors):
        misure = []
        for _ in range(n_misure):
            try:
                d = sensor.range
                misure.append(d)
            except Exception as e:
                print(f"Errore lettura {nome}: {e}")
                break
        distanze[nome] = int(sum(misure) / len(misure)) if misure else None

    return distanze

# --- Loop principale ---
if __name__ == '__main__':
    try:
        while True:
            d = leggi_distanze_doppie()
            print(d)
            time.sleep(0.005)
    except KeyboardInterrupt:
        print("Interrotto manualmente.")
    finally:
        GPIO.cleanup()
        bus.close()
