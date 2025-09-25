import time
import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_vl53l0x

# Mappatura sensori: indirizzo I2C → (nome ruolo, pin fisico)
sensor_info = {
    0x30: ("FL", "GPIO 17"),
    0x31: ("FR", "GPIO 27"),
    0x32: ("R1", "GPIO 22"),
    0x33: ("R2", "GPIO 6")
}

xshut_pins = [board.D17, board.D27, board.D22, board.D6]
sensor_addresses = list(sensor_info.keys())
sensors = []
sensor_roles = {}

def reset_sensori():
    print("🛠️ Reset hardware dei sensori via XSHUT...\n")
    xshut_controls = []
    for pin in xshut_pins:
        ctrl = DigitalInOut(pin)
        ctrl.direction = Direction.OUTPUT
        ctrl.value = False
        xshut_controls.append(ctrl)

    time.sleep(0.2)

    for i, ctrl in enumerate(xshut_controls):
        ctrl.value = True
        print(f"  → Sensore {i+1} riacceso")
        time.sleep(0.1)
    print()

def inizializza_sensori():
    global sensors, sensor_roles
    i2c = busio.I2C(board.SCL, board.SDA)
    xshut_controls = []

    for pin in xshut_pins:
        ctrl = DigitalInOut(pin)
        ctrl.direction = Direction.OUTPUT
        ctrl.value = False
        xshut_controls.append(ctrl)

    time.sleep(0.2)

    sensori_rilevati = []

    for i, address in enumerate(sensor_addresses):
        role, gpio = sensor_info[address]
        ctrl = xshut_controls[i]

        try:
            ctrl.value = True
            time.sleep(0.05)
            sensor = adafruit_vl53l0x.VL53L0X(i2c)
            sensor.set_address(address)
            sensor.start_continuous()
            sensors.append(sensor)
            sensor_roles[role] = sensor
            sensori_rilevati.append(f"{role} ({hex(address)}, {gpio})")
            print(f"  ✅ {role} inizializzato a {hex(address)} ({gpio})")
        except Exception:
            print(f"  ⛔ Impossibile inizializzare {role} ({hex(address)}, {gpio})")
    print()
    if sensori_rilevati:
        print(f"✅ {len(sensori_rilevati)} sensori rilevati correttamente: {', '.join(sensori_rilevati)}")
    else:
        raise RuntimeError("❌ Nessun sensore VL53L0X inizializzato. Verifica il cablaggio.")

def leggi_distanze():
    ruoli = ["FL", "FR", "R1", "R2"]
    distanze = {}

    for ruolo in ruoli:
        sensor = sensor_roles.get(ruolo)
        try:
            distanze[ruolo] = sensor.range if sensor else None
        except Exception:
            distanze[ruolo] = None

    if distanze['R2'] is not None:
        distanze['R2'] -= 38
    if distanze['FL'] is not None:
        distanze['FL'] += 40

    return distanze

# Inizializzazione automatica
reset_sensori()
inizializza_sensori()

# Test interattivo
if __name__ == "__main__":
    print("\n📊 Lettura continua dei sensori (Ctrl+C per uscire)")
    try:
        while True:
            d = leggi_distanze()
            print("\n             [ FRONT ]")
            print(f"        [FL]         [FR]")
            print(f"       {d['FL'] or '----':>5} mm  {d['FR'] or '----':>5} mm")
            print("       -------------------")
            print("       |                 |")
            print("       |                 |  [R1]")
            print(f"       |                 | {d['R1'] or '----':>5} mm")
            print("       |                 |")
            print("       |                 |  [R2]")
            print(f"       |                 | {d['R2'] or '----':>5} mm")
            print("       -------------------")
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\n🛑 Uscita dal programma.")
