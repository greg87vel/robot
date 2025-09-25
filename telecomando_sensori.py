import RPi.GPIO as GPIO
import time
import keyboard
from sensori import leggi_distanze  # funzione già gestita con try/except interno

vel = 100

# Pin motori
MOTORDX_IN1 = 21
MOTORDX_IN2 = 20
MOTORSX_IN1 = 26
MOTORSX_IN2 = 19

PWM_FREQ = 6000

GPIO.setmode(GPIO.BCM)
GPIO.setup([MOTORSX_IN1, MOTORSX_IN2, MOTORDX_IN1, MOTORDX_IN2], GPIO.OUT)

motorsx_pwm1 = GPIO.PWM(MOTORSX_IN1, PWM_FREQ)
motorsx_pwm2 = GPIO.PWM(MOTORSX_IN2, PWM_FREQ)
motordx_pwm1 = GPIO.PWM(MOTORDX_IN1, PWM_FREQ)
motordx_pwm2 = GPIO.PWM(MOTORDX_IN2, PWM_FREQ)

motorsx_pwm1.start(0)
motorsx_pwm2.start(0)
motordx_pwm1.start(0)
motordx_pwm2.start(0)

def accosta_destra(speed):
    motorsx_pwm1.ChangeDutyCycle(speed - 1)
    motorsx_pwm2.ChangeDutyCycle(0)
    motordx_pwm1.ChangeDutyCycle(speed - 10)
    motordx_pwm2.ChangeDutyCycle(0)

def accosta_sinistra(speed):
    motorsx_pwm1.ChangeDutyCycle(speed - 10)
    motorsx_pwm2.ChangeDutyCycle(0)
    motordx_pwm1.ChangeDutyCycle(speed - 1)
    motordx_pwm2.ChangeDutyCycle(0)

def svolta_sinistra(vel):
    motorsx_pwm1.ChangeDutyCycle(vel)
    motorsx_pwm2.ChangeDutyCycle(0)
    motordx_pwm1.ChangeDutyCycle(0)
    motordx_pwm2.ChangeDutyCycle(vel)

def svolta_destra(vel):
    motorsx_pwm1.ChangeDutyCycle(0)
    motorsx_pwm2.ChangeDutyCycle(vel)
    motordx_pwm1.ChangeDutyCycle(vel)
    motordx_pwm2.ChangeDutyCycle(0)

def avanti(speed):
    motorsx_pwm2.ChangeDutyCycle(speed)
    motorsx_pwm1.ChangeDutyCycle(0)
    motordx_pwm2.ChangeDutyCycle(speed)
    motordx_pwm1.ChangeDutyCycle(0)

def indietro(speed):
    motorsx_pwm1.ChangeDutyCycle(speed)
    motorsx_pwm2.ChangeDutyCycle(0)
    motordx_pwm1.ChangeDutyCycle(speed)
    motordx_pwm2.ChangeDutyCycle(0)

def stop():
    motorsx_pwm2.ChangeDutyCycle(0)
    motorsx_pwm1.ChangeDutyCycle(0)
    motordx_pwm2.ChangeDutyCycle(0)
    motordx_pwm1.ChangeDutyCycle(0)

def chiudi():
    motorsx_pwm1.stop()
    motorsx_pwm2.stop()
    motordx_pwm1.stop()
    motordx_pwm2.stop()
    GPIO.cleanup()
    print("\nChiusura e pulizia GPIO.")

def stampa_distanze():
    try:
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
    except Exception as e:
        print(f"⚠️ Errore lettura sensori: {e}")

# Ciclo principale
if __name__ == "__main__":
    try:
        while True:
            movimento = False

            if keyboard.is_pressed('up'):
                avanti(vel)
                movimento = True
            elif keyboard.is_pressed('down'):
                indietro(vel)
                movimento = True
            elif keyboard.is_pressed('left'):
                svolta_sinistra(vel)
                movimento = True
            elif keyboard.is_pressed('right'):
                svolta_destra(vel)
                movimento = True
            else:
                stop()

            if movimento:
                time.sleep(0.05)  # attesa breve per stabilizzare tensione
                stampa_distanze()

            time.sleep(0.05)

    except KeyboardInterrupt:
        chiudi()
