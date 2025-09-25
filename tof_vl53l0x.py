import time
import board
from digitalio import DigitalInOut, Direction
import adafruit_vl53l0x

# GPIO usati per XSHUT (uno per sensore)
xshut_pins = [board.D17, board.D27, board.D22, board.D6]

# Inizializzazione dei pin XSHUT
xshut_controls = []
for pin in xshut_pins:
    ctrl = DigitalInOut(pin)
    ctrl.direction = Direction.OUTPUT
    ctrl.value = False  # Spegne il sensore
    xshut_controls.append(ctrl)

# Inizializza il bus I2C
i2c = board.I2C()

# Indirizzi I2C assegnati ai sensori
sensor_addresses = [0x30, 0x31, 0x32, 0x33]

# Lista dei sensori
sensors = []

# Attiva e configura i sensori uno alla volta
for i, ctrl in enumerate(xshut_controls):
    # Accende il sensore
    ctrl.value = True
    time.sleep(0.05)  # attesa per la stabilizzazione

    # Inizializza il sensore (all'indirizzo 0x29)
    sensor = adafruit_vl53l0x.VL53L0X(i2c)

    # Imposta un indirizzo univoco
    sensor.set_address(sensor_addresses[i])

    # Avvia la modalità continua (default: ~30ms tra le misure)
    sensor.start_continuous()

    # Aggiunge alla lista
    sensors.append(sensor)

# Loop di lettura in modalità continua
print("Lettura in modalità continua (Ctrl+C per uscire)")

try:
    while True:
        # Letture sensori
        front_left  = sensors[0].range  # GPIO 17
        front_right = sensors[1].range  # GPIO 27
        right_front = sensors[2].range  # GPIO 22
        right_rear  = sensors[3].range  # GPIO 6

        # Stampa a pianta
        print("\n             [ FRONT ]")
        print(f"        [FL]         [FR]")
        print(f"       {front_left:>5} mm      {front_right:>5} mm")
        print("       -------------------")
        print("       |                 |")
        print("       |                 |  [R1]")
        print(f"       |                 | {right_front:>5} mm")
        print("       |                 |")
        print("       |                 |  [R2]")
        print(f"       |                 | {right_rear:>5} mm")
        print("       -------------------")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nUscita dal programma.")


