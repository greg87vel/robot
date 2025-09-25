from motori import avanti, indietro, stop, chiudi, accosta_destra, accosta_sinistra, gira_destra, gira_sinistra
from tof import leggi_distanze
from buzzer import suona_buzzer
import time
import RPi.GPIO as GPIO
from enum import Enum
from infrarossi import stato_ir_davanti_dx, stato_ir_davanti_sx

# === COSTANTI ===
VEL = 70
DISTANZA_DESIDERATA = 120
TOLLERANZA = 10            

DISTANZA_OSTACOLO = 255
LED = 24
PAUSA = 0.01

# === STATI ===
class Stato(Enum):
    RICERCA_MURO = 1
    SEGUI_MURO = 2
    EVITA_OSTACOLO = 3


def stampa_info():
    # STAMPO LE INFORMAZIONI IN CONSOLE
    print("VELOCITA': ", VEL)
    
    
def leggi_sensori():
    lista_distanze = leggi_distanze()
    return {
        'da' : lista_distanze[0],
        'dp' : lista_distanze[1],
    }
    
stato = Stato.RICERCA_MURO    
if __name__ == '__main__':
    
    try:
        
        while True:
            
            distanze = leggi_sensori()
            davanti_dx = stato_ir_davanti_dx()
            davanti_sx = stato_ir_davanti_sx()
            
            if stato == Stato.RICERCA_MURO:
                if davanti_dx == 0 or davanti_sx == 0:
                    stato = Stato.EVITA_OSTACOLO
                else:
                    print('avanti')
                    avanti(VEL)
        
           
                    
#################################################################################################

            elif stato == Stato.SEGUI_MURO:
                if davanti_dx == 0 or davanti_sx == 0:
                    stato = Stato.EVITA_OSTACOLO
                else:
                    distanza_media_dx = (distanze['da'] + distanze['dp']) / 2
                    if distanza_media_dx > DISTANZA_DESIDERATA + TOLLERANZA:
                        print('accosta destra')
                        accosta_destra(VEL)
                    elif distanza_media_dx < DISTANZA_DESIDERATA - TOLLERANZA:
                        print ('accosta sinistra')
                        accosta_sinistra(VEL)
                    else:
                        print('avanti')
                        avanti(VEL)

            elif stato == Stato.EVITA_OSTACOLO:
                if davanti_dx == 1 or davanti_sx == 1:
                    stato = Stato.SEGUI_MURO
                else:
                    print('gira sinistra')
                    gira_sinistra(VEL)
            
            print()
            print(stato.name)
            print(distanze)
            time.sleep(PAUSA)  # loop delay
            
            
                
                
                
        
            #time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("Interrotto manualmente.")

    finally:
        GPIO.cleanup()
