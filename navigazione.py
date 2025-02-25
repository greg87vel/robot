from motori import avanti, indietro, stop, chiudi
from sonar import misura_distanza, media_distanze
from fotoresistenza import valore_fotoresistenza
from buzzer import suona_buzzer
import time
import RPi.GPIO as GPIO


# INIZIALIZZAZIONE DEI PIN DI INPUT E OUTPUT

FOTORES = 4
PULSANTE_AVVIO = 25
LED = 24
BUZZER = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(PULSANTE_AVVIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(FOTORES, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)


# INIZIAMO IN MODALITA' STANDBY
stato_attivo = False

try:
    
    while True:
        
        time.sleep(1)    
        print("\nPremi il pulsante per iniziare...")
        
        # ATTENDO CHE VENGA PREMUTO IL PULSANTE DI AVVIO
        while GPIO.input(PULSANTE_AVVIO) == 1:
            GPIO.output(LED, GPIO.HIGH)
            time.sleep(0.1)
        
        # ESCO DALLA MODALITA' STANDBY
        print("Avvio...")
        stato_attivo = True
        
        # MENTRE SONO IN MODALITA' ATTIVA:
        while stato_attivo == True:
            
            # MISURO LA DISTANZA COL SONAR E DI CONSEGUENZA IMPOSTO LA VELOCITA' DEI MOTORI
            dist = misura_distanza()
            speed = 6 * dist - 170             
                  
            # SE LA VELOCITA' E' POSITIVA VADO AVANTI
            if speed > 0:
                if speed > 100:
                    speed =  100
                avanti(speed)
            
            # SE LA VELOCITA' E' NEGATIVA VADO INDIETRO
            elif speed < 0:
                if speed < -100:
                    speed = -100
                indietro(abs(speed))
            
            # SE LA VELOCITA' E' ZERO MI FERMO
            else:
                stop()

            # STAMPO LE INFORMAZIONI IN CONSOLE
            print("\nPULSANTE: ", GPIO.input(PULSANTE_AVVIO))
            print("FOTORESISTENZA: ", valore_fotoresistenza())
            print("VELOCITA': ", speed)
            
            # CAMBIO LO STATO DEL LED AD OGNI CICLO PER FARLO LAMPEGGIARE
            GPIO.output(LED, not GPIO.input(LED))
            
            time.sleep(0.1)
            
            # SE PREMO IL PULSANTE OPPURE LA FOTORESISTENZA RILEVA UNA FORTE LUCE TORNO IN STANDBY
            if GPIO.input(PULSANTE_AVVIO) == 0:
                stop()
                print("\nStop")
                stato_attivo = False
                
            if valore_fotoresistenza() == 1:
                stop()
                print("\nRilevata luce")
                print("\nMi fermo ed emetto un suono di avviso")
                suona_buzzer(5)
                time.sleep(3)
                
        
except KeyboardInterrupt:
    chiudi()
    
