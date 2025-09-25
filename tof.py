import time
import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_vl53l0x

# Pin XSHUT secondo la mappatura board.Dxx
xshut_pins = [board.D17, board.D27, board.D22, board.D6]
sensor_addresses = [0x30, 0x31, 0x32, 0x33]
sensors = []

def reset_sensori():
    print("🛠️ Reset hardware dei sensori via XSHUT...")
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

def inizializza_sensori():
    global sensors
    i2c = busio.I2C(board.SCL, board.SDA)

    try:
        print("🔧 Avvio inizializzazione standard...")
        xshut_controls = []
        for pin in xshut_pins:
            ctrl = DigitalInOut(pin)
            ctrl.direction = Direction.OUTPUT
            ctrl.value = False
            xshut_controls.append(ctrl)

        time.sleep(0.2)

        for i, ctrl in enumerate(xshut_controls):
            ctrl.value = True
            time.sleep(0.05)
            sensor = adafruit_vl53l0x.VL53L0X(i2c)
            sensor.set_address(sensor_addresses[i])
            sensor.start_continuous()
            sensors.append(sensor)

        print("✅ Sensori inizializzati con nuovi indirizzi.")

    except Exception as e:
        print("⚠️  Configurazione fallita, provo il rilevamento automatico...")

        for address in sensor_addresses:
            try:
                sensor = adafruit_vl53l0x.VL53L0X(i2c, address=address)
                sensor.start_continuous()
                sensors.append(sensor)
            except Exception:
                print(f"  ⛔ Nessun sensore all'indirizzo {hex(address)}")

        if sensors:
            print(f"✅ {len(sensors)} sensori rilevati automaticamente.")
        else:
            raise RuntimeError("❌ Nessun sensore VL53L0X trovato. Verifica il cablaggio.")

def leggi_distanze():
    labels = ["FR", "FL", "R1", "R2"]
    distanze = {}
    for i, label in enumerate(labels):
        if i < len(sensors):
            distanze[label] = sensors[i].range
        else:
            distanze[label] = None
    distanze['R2'] -= 38
    distanze['FL'] += 40
    return distanze

# Inizializzazione automatica
reset_sensori()
inizializza_sensori()

# Test interattivo
if __name__ == "__main__":
    print("📊 Lettura continua dei sensori (Ctrl+C per uscire)")
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
