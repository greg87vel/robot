import time
import smbus2
import RPi.GPIO as GPIO
import board
import busio
import adafruit_vl6180x

# --- Configurazioni ---
I2C_BUS = 1
DEFAULT_ADDRESS = 0x29
NEW_ADDRESSES = [0x30, 0x31, 0x32, 0x33]
SHDN_PINS = [17, 27, 13, 16]

# --- Inizializza il bus I2C per smbus2 (per setup avanzato) ---
bus = smbus2.SMBus(I2C_BUS)

# --- Inizializza il bus I2C per Adafruit (per lettura sensori) ---
i2c = busio.I2C(board.SCL, board.SDA)

# --- Setup dei pin GPIO per SHDN ---
GPIO.setmode(GPIO.BCM)
for pin in SHDN_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Spegne tutti i sensori

time.sleep(0.1)

# --- Funzioni di supporto ---
def sensor_on(index):
    GPIO.output(SHDN_PINS[index], GPIO.HIGH)
    time.sleep(0.05)

def sensor_off(index):
    GPIO.output(SHDN_PINS[index], GPIO.LOW)
    time.sleep(0.01)

def read_byte(addr, reg):
    return bus.read_byte_data(addr, reg)

def write_byte(addr, reg, val):
    bus.write_byte_data(addr, reg, val)

def write_word(addr, reg, val):
    """Scrive una word (16 bit) al registro"""
    data = [(reg >> 8) & 0xFF, reg & 0xFF, val]
    write = smbus2.i2c_msg.write(addr, data)
    bus.i2c_rdwr(write)

def change_address(old_addr, new_addr):
    """Cambia l'indirizzo I2C del sensore"""
    write_word(old_addr, 0x0212, new_addr)
    time.sleep(0.01)

def init_sensor(addr):
    """
    Inizializza il VL6180X con i valori standard per il funzionamento base.
    """
    try:
        # Mandatory : Private registers
        write_byte(addr, 0x0207, 0x01)
        write_byte(addr, 0x0208, 0x01)
        write_byte(addr, 0x0096, 0x00)
        write_byte(addr, 0x0097, 0xfd)
        write_byte(addr, 0x00e3, 0x00)
        write_byte(addr, 0x00e4, 0x04)
        write_byte(addr, 0x00e5, 0x02)
        write_byte(addr, 0x00e6, 0x01)
        write_byte(addr, 0x00e7, 0x03)
        write_byte(addr, 0x00f5, 0x02)
        write_byte(addr, 0x00d9, 0x05)
        write_byte(addr, 0x00db, 0xce)
        write_byte(addr, 0x00dc, 0x03)
        write_byte(addr, 0x00dd, 0xf8)
        write_byte(addr, 0x009f, 0x00)
        write_byte(addr, 0x00a3, 0x3c)
        write_byte(addr, 0x00b7, 0x00)
        write_byte(addr, 0x00bb, 0x3c)
        write_byte(addr, 0x00b2, 0x09)
        write_byte(addr, 0x00ca, 0x09)
        write_byte(addr, 0x0198, 0x01)
        write_byte(addr, 0x01b0, 0x17)
        write_byte(addr, 0x01ad, 0x00)
        write_byte(addr, 0x00ff, 0x05)
        write_byte(addr, 0x0100, 0x05)
        write_byte(addr, 0x0199, 0x05)
        write_byte(addr, 0x01a6, 0x1b)
        write_byte(addr, 0x01ac, 0x3e)
        write_byte(addr, 0x01a7, 0x1f)
        write_byte(addr, 0x0030, 0x00)

        # Recommended: Public registers
        write_byte(addr, 0x0011, 0x10)
        write_byte(addr, 0x010a, 0x30)
        write_byte(addr, 0x003f, 0x46)
        write_byte(addr, 0x0031, 0xFF)
        write_byte(addr, 0x0040, 0x63)
        write_byte(addr, 0x002e, 0x01)

        # Optional: Additional settings
        write_byte(addr, 0x001b, 0x09)
        write_byte(addr, 0x003e, 0x31)
        write_byte(addr, 0x0014, 0x24)

        print(f"Sensore {hex(addr)} inizializzato correttamente.")
    except Exception as e:
        print(f"Errore inizializzazione sensore {hex(addr)}: {e}")

# --- Reset di tutti i sensori ---
for i in range(4):
    sensor_off(i)
time.sleep(0.5)

# --- Assegna nuovi indirizzi ai sensori ---
for i, new_addr in enumerate(NEW_ADDRESSES):
    print(f"\nAccensione sensore {i} sul GPIO {SHDN_PINS[i]}")
    sensor_on(i)
    time.sleep(0.1)

    try:
        model_id = read_byte(DEFAULT_ADDRESS, 0x000)
        print(f"Model ID letto: {hex(model_id)} dal sensore {i}")

        change_address(DEFAULT_ADDRESS, new_addr)
        print(f"Indirizzo cambiato a {hex(new_addr)}")

        init_sensor(new_addr)
    except Exception as e:
        print(f"Errore durante setup sensore {i}: {e}")

# --- Crea istanze Adafruit per ogni sensore ---
sensors = []
for addr in NEW_ADDRESSES:
    try:
        sensor = adafruit_vl6180x.VL6180X(i2c, address=addr)
        sensors.append(sensor)
        print(f"Sensore Adafruit creato su indirizzo {hex(addr)}")
    except Exception as e:
        print(f"Errore creazione istanza Adafruit per il sensore {hex(addr)}: {e}")


def leggi_distanze():
    lista_distanze = []
    for i, sensor in enumerate(sensors):
        try:
            distance = sensor.range  # Misura la distanza in mm
            lista_distanze.append(distance)
            #print(f"Sensore {hex(NEW_ADDRESSES[i])}: {distance} mm")
        except Exception as e:
            print(f"Errore lettura sensore {hex(NEW_ADDRESSES[i])}: {e}")
            
    return lista_distanze


if __name__ == '__main__':
    
    # --- Ciclo di lettura delle distanze ---
    try:
        while True:
            distanze = leggi_distanze()

            print("----")
            print(distanze)
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Interrotto manualmente.")

    finally:
        GPIO.cleanup()
        bus.close()
