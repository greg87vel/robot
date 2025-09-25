import time
from motori import gira_sinistra, stop, chiudi, aggira_angolo_destro, set_motore_sinistra, set_motore_destra
from tof import leggi_distanze
from fototransistor import rilevamento_luce
from buzzer import suona_buzzer

# Velocità
SPEED = 100
MIN_SPEED = 50

# Parametri muro
SOGLIA_FRONTALE = 240
DISTANZA_MURO = 100
TOLLERANZA = 20
TEMPO_SUPERAMENTO = 0.3
TEMPO_AGGIRAMENTO = 0.5

# Guadagni
Kp_align = 0.8
Kd_align = 0.15
Kp_dist = -0.8
ERRORE_RIDUZIONE_VELOCITA = 50

# Stati
STATE_AVANZA = "AVANZA"
STATE_ALLINEAMENTO = "ALLINEAMENTO"
STATE_SEGUI_MURO = "SEGUI_MURO"
STATE_MURO_ALLINEAMENTO = "MURO_ALLINEAMENTO"
STATE_MURO_DISTANZA = "MURO_DISTANZA"
STATE_AGGIRA_ANGOLO_DX = "AGGIRA_ANGOLO_DX"
STATE_AGGIRA_ANGOLO_AVANZA = "AGGIRA_ANGOLO_AVANZA"
STATE_AGGIRA_ANGOLO_RUOTA = "AGGIRA_ANGOLO_RUOTA"
STATE_AGGIRA_ANGOLO_RECUPERA = "AGGIRA_ANGOLO_RECUPERA"
STATE_RILEVAMENTO_LUCE = "RILEVAMENTO_LUCE"

def main():
    i = 0
    ultimo_rilevamento = 0
    
    stato = STATE_AVANZA
    errore_precedente = 0
    aggira_inizio_tempo = None

    print("🤖 Avvio logica con controllo PD su distanza e allineamento del muro")

    
    while True:
        fototransistor = rilevamento_luce()
        if 1 in fototransistor and time.time() - ultimo_rilevamento > 10:
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
                set_motore_destra(SPEED)                            +

        elif stato == STATE_ALLINEAMENTO:
            if (fl > SOGLIA_FRONTALE) and (fr > SOGLIA_FRONTALE):
                stato = STATE_MURO_ALLINEAMENTO
                i = 0
            else:
                gira_sinistra(70)
                i += 1
                if i > 100:
                    i = 0
                    stato = STATE_AVANZA

        elif stato == STATE_SEGUI_MURO:
            stato = STATE_MURO_ALLINEAMENTO

        elif stato == STATE_MURO_ALLINEAMENTO:
            if (fl < SOGLIA_FRONTALE) or (fr < SOGLIA_FRONTALE):
                print("🧱 Muro rilevato di fronte, ruoto a sinistra")
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
                print("🧱 Muro rilevato di fronte, ruoto a sinistra")
                stop()
                time.sleep(0.1)
                stato = STATE_ALLINEAMENTO
                continue
            stop()
            aggira_inizio_tempo = time.time()
            stato = STATE_AGGIRA_ANGOLO_AVANZA

        elif stato == STATE_AGGIRA_ANGOLO_AVANZA:
            if (fl < SOGLIA_FRONTALE) or (fr < SOGLIA_FRONTALE):
                print("🧱 Muro rilevato di fronte, ruoto a sinistra")
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
                print("🧱 Muro rilevato di fronte, ruoto a sinistra")
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
            suona_buzzer(5)
            stato = STATE_SEGUI_MURO

        time.sleep(0.05)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Interruzione Manuale (Ctrl+C)")
        stop()
        chiudi()
