import time
import board
import busio
import adafruit_vl6180x

# --- Inizializzazione I2C e sensore ---
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl6180x.VL6180X(i2c)

def leggi_distanze(n_misure=5):
    """Lettura veloce con media su più misure"""
    misure = []
    for _ in range(n_misure):
        try:
            distanza = sensor.range  # Misura in mm
            misure.append(distanza)
        except Exception as e:
            print(f"Errore durante la lettura: {e}")
            break
    if misure:
        return int(sum(misure) / len(misure))
    else:
        return None

if __name__ == '__main__':
    try:
        while True:
            distanza = leggi_distanze(n_misure=5)  # Regola n_misure per velocità/precisione
            print(f"Distanza: {distanza} mm")
            time.sleep(0.005)  # Pausa minima per evitare blocchi del bus
    except KeyboardInterrupt:
        print("Interrotto manualmente.")
