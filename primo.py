import time
import RPi.GPIO as GPIO
from motori import gira_sinistra, stop, chiudi, aggira_angolo_destro, set_motore_sinistra, set_motore_destra
from tof import leggi_distanze
from fototransistor import rilevamento_luce
from buzzer import suona_buzzer

# GPIO
PIN_LED = 14
PIN_BUTTON = 18

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
time.sleep(0.1)
GPIO.setup(PIN_LED, GPIO.OUT)
GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Stati
SPEED = 100
SOGLIA_FRONTALE = 240
DISTANZA_MURO = 100
TEMPO_SUPERAMENTO = 0.3
TEMPO_AGGIRAMENTO = 0.5
Kp_align = 0.8
Kd_align = 0.15
Kp_dist = -0.8

STATE_AVANZA = "AVANZA"
STATE_ALLINEAMENTO = "ALLINEAMENTO"
STATE_SEGUI_MURO = "SEGUI_MURO"
STATE_MURO_ALLINEAMENTO = "MURO_ALLINEAMENTO"
STATE_AGGIRA_ANGOLO_DX = "AGGIRA_ANGOLO_DX"
STATE_AGGIRA_ANGOLO_AVANZA = "AGGIRA_ANGOLO_AVANZA"
STATE_AGGIRA_ANGOLO_RUOTA = "AGGIRA_ANGOLO_RUOTA"
STATE_RILEVAMENTO_LUCE = "RILEVAMENTO_LUCE"

# Stato globale
attivo = False
errore_precedente = 0
stato = STATE_AVANZA
ultimo_rilevamento = 0
aggira_inizio_tempo = None

# LED
led_on = False
last_led_toggle = time.time()

# Pulsante
stato_pulsante_precedente = GPIO.input(PIN_BUTTON)

print("🛑 Sistema in standby")
GPIO.output(PIN_LED, GPIO.HIGH)

try:
    while True:
        now = time.time()

        # Toggle LED se attivo
        if attivo and now - last_led_toggle >= 0.5:
            led_on = not led_on
            GPIO.output(PIN_LED, GPIO.HIGH if led_on else GPIO.LOW)
            last_led_toggle = now

        # Pulsante
        stato_pulsante_attuale = GPIO.input(PIN_BUTTON)
        if stato_pulsante_precedente == GPIO.HIGH and stato_pulsante_attuale == GPIO.LOW:
            if not attivo:
                print("▶️ Avvio")
                attivo = True
                stato = STATE_AVANZA
                errore_precedente = 0
                ultimo_rilevamento = 0
                aggira_inizio_tempo = None
                GPIO.output(PIN_LED, GPIO.LOW)
                last_led_toggle = now
            else:
                print("⏹️ Arresto")
                attivo = False
                stop()
                GPIO.output(PIN_LED, GPIO.HIGH)
            time.sleep(0.2)
        stato_pulsante_precedente = stato_pulsante_attuale

        # Logica robot attiva solo se in esecuzione
        if attivo:
            fototransistor = rilevamento_luce()
            if 1 in fototransistor and (time.time()-ultimo_rilevamento) > 10:
                print("🔦 RILEVATO OBIETTIVO!")
                ultimo_rilevamento = time.time()
                stato = STATE_RILEVAMENTO_LUCE

            distanze = leggi_distanze()
            fl = distanze.get("FL")
            fr = distanze.get("FR")
            r1 = distanze.get("R1")
            r2 = distanze.get("R2")

            print(f"\n📡 Stato: {stato}")
            print(f"    FL = {fl} mm, FR = {fr} mm, R1 = {r1} mm, R2 = {r2} mm")
            print(f"    Fototransistor: {fototransistor[0]} - {fototransistor[1]}")

            if stato == STATE_AVANZA:
                if (fl < SOGLIA_FRONTALE) or (fr < SOGLIA_FRONTALE):
                    stop()
                    stato = STATE_ALLINEAMENTO
                else:
                    set_motore_sinistra(SPEED)
                    set_motore_destra(SPEED)

            elif stato == STATE_ALLINEAMENTO:
                if (fl > SOGLIA_FRONTALE) and (fr > SOGLIA_FRONTALE):
                    stato = STATE_MURO_ALLINEAMENTO
                else:
                    gira_sinistra(100)

            elif stato == STATE_SEGUI_MURO:
                stato = STATE_MURO_ALLINEAMENTO

            elif stato == STATE_MURO_ALLINEAMENTO:
                if (fl < SOGLIA_FRONTALE) or (fr < SOGLIA_FRONTALE):
                    print("🧱 Muro di fronte")
                    stop()
                    time.sleep(0.1)
                    stato = STATE_ALLINEAMENTO
                    continue

                if fl > SOGLIA_FRONTALE and r1 > 300:
                    stato = STATE_AGGIRA_ANGOLO_DX
                    continue

                errore_allineamento = r1 - r2
                errore_distanza = DISTANZA_MURO - (r1 + r2) / 2
                derivata_allineamento = errore_allineamento - errore_precedente
                errore_precedente = errore_allineamento

                correzione = (
                    Kp_align * errore_allineamento +
                    Kd_align * derivata_allineamento +
                    Kp_dist * errore_distanza
                )

                motore_sx = max(-100, min(100, SPEED + correzione))
                motore_dx = max(-100, min(100, SPEED - correzione))

                set_motore_sinistra(motore_sx)
                set_motore_destra(motore_dx)

            elif stato == STATE_AGGIRA_ANGOLO_DX:
                if (fl < SOGLIA_FRONTALE) or (fr < SOGLIA_FRONTALE):
                    stop()
                    time.sleep(0.1)
                    stato = STATE_ALLINEAMENTO
                    continue
                stop()
                aggira_inizio_tempo = time.time()
                stato = STATE_AGGIRA_ANGOLO_AVANZA

            elif stato == STATE_AGGIRA_ANGOLO_AVANZA:
                if (fl < SOGLIA_FRONTALE) or (fr < SOGLIA_FRONTALE):
                    stop()
                    time.sleep(0.1)
                    stato = STATE_ALLINEAMENTO
                    continue
                set_motore_sinistra(SPEED)
                set_motore_destra(SPEED)
                if time.time() - aggira_inizio_tempo > TEMPO_SUPERAMENTO:
                    stop()
                    aggira_inizio_tempo = time.time()
                    stato = STATE_AGGIRA_ANGOLO_RUOTA

            elif stato == STATE_AGGIRA_ANGOLO_RUOTA:
                if (fl < SOGLIA_FRONTALE) or (fr < SOGLIA_FRONTALE):
                    stop()
                    time.sleep(0.1)
                    stato = STATE_ALLINEAMENTO
                    continue
                set_motore_sinistra(SPEED)
                set_motore_destra(0)
                if time.time() - aggira_inizio_tempo > TEMPO_AGGIRAMENTO:
                    stop()
                    stato = STATE_SEGUI_MURO

            elif stato == STATE_RILEVAMENTO_LUCE:
                stop()
                suona_buzzer(8)
                stato = STATE_SEGUI_MURO

        time.sleep(0.05)

except KeyboardInterrupt:
    print("Uscita manuale")
finally:
    stop()
    chiudi()
    GPIO.cleanup()
