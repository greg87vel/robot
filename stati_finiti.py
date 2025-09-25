import time
from enum import Enum

# === COSTANTI ===
DISTANZA_DESIDERATA = 150  # in mm
TOLLERANZA = 30             # in mm
DISTANZA_OSTACOLO = 120    # in mm

# === STATI ===
class Stato(Enum):
    RICERCA_MURO = 1
    ALLINEAMENTO = 2
    SEGUI_MURO = 3
    EVITA_OSTACOLO = 4

# === MOCKUP SENSORI ===
def leggi_sensori():
    return {
        'frontale_dx':  get_distanza('FDX'),
        'frontale_sx':  get_distanza('FSX'),
        'laterale_dx_ant': get_distanza('LDXA'),
        'laterale_dx_post': get_distanza('LDXP'),
    }

# === CONTROLLO MOTORI ===
def avanti():
    set_motori(vel_sx=0.5, vel_dx=0.5)

def ferma():
    set_motori(0, 0)

def gira_destra():
    set_motori(0.3, -0.3)

def gira_sinistra():
    set_motori(-0.3, 0.3)

def curva_leggera_destra():
    set_motori(0.5, 0.4)

def curva_leggera_sinistra():
    set_motori(0.4, 0.5)
    

# === LOGICA FSM ===
stato = Stato.RICERCA_MURO


while True:
    distanze = leggi_sensori()

    if stato == Stato.RICERCA_MURO:
        if distanze['laterale_dx_ant'] < 300:
            stato = Stato.ALLINEAMENTO
        else:
            gira_destra()

    elif stato == Stato.ALLINEAMENTO:
        diff = abs(distanze['laterale_dx_ant'] - distanze['laterale_dx_post'])
        if diff < 30:
            stato = Stato.SEGUI_MURO
        elif distanze['laterale_dx_ant'] > distanze['laterale_dx_post']:
            gira_sinistra()
        else:
            gira_destra()

    elif stato == Stato.SEGUI_MURO:
        if distanze['frontale_dx'] < DISTANZA_OSTACOLO or distanze['frontale_sx'] < DISTANZA_OSTACOLO:
            stato = Stato.EVITA_OSTACOLO
        else:
            distanza_media_dx = (distanze['laterale_dx_ant'] + distanze['laterale_dx_post']) / 2
            if distanza_media_dx > DISTANZA_DESIDERATA + TOLLERANZA:
                curva_leggera_destra()
            elif distanza_media_dx < DISTANZA_DESIDERATA - TOLLERANZA:
                curva_leggera_sinistra()
            else:
                avanti()

    elif stato == Stato.EVITA_OSTACOLO:
        gira_sinistra()
        time.sleep(0.6)
        avanti()
        time.sleep(0.5)
        gira_destra()
        time.sleep(0.6)
        stato = Stato.RICERCA_MURO

    time.sleep(0.1)  # loop delay

# === FUNZIONI DA IMPLEMENTARE ===
def get_distanza(sensore_id):
    # Leggi e ritorna distanza in mm da un dato sensore
    pass

def set_motori(vel_sx, vel_dx):
    # Imposta le velocità dei motori sinistro e destro (-1 a 1)
    pass
