import RPi.GPIO as GPIO
import time
import keyboard  # Modulo per leggere i tasti della tastiera

vel = 100

# Definizione dei pin per i motori
MOTORSX_IN1 = 20  # GPIO per direzione motore 1
MOTORSX_IN2 = 21  # GPIO per direzione motore 1
MOTORDX_IN1 = 19  # GPIO per direzione motore 2
MOTORDX_IN2 = 26  # GPIO per direzione motore 2

# Frequenza PWM
PWM_FREQ = 6000  # Hz

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup([MOTORSX_IN1, MOTORSX_IN2, MOTORDX_IN1, MOTORDX_IN2], GPIO.OUT)

# Creazione degli oggetti PWM
motorsx_pwm1 = GPIO.PWM(MOTORSX_IN1, PWM_FREQ)
motorsx_pwm2 = GPIO.PWM(MOTORSX_IN2, PWM_FREQ)
motordx_pwm1 = GPIO.PWM(MOTORDX_IN1, PWM_FREQ)
motordx_pwm2 = GPIO.PWM(MOTORDX_IN2, PWM_FREQ)

# Avvio dei PWM con duty cycle a 0 (fermi)
motorsx_pwm1.start(0)
motorsx_pwm2.start(0)
motordx_pwm1.start(0)
motordx_pwm2.start(0)

# Funzione per impostare la velocità dei motori
def set_motor_speed(motor_pwm1, motor_pwm2, speed):
    if speed > 0:
        motor_pwm1.ChangeDutyCycle(speed)
        motor_pwm2.ChangeDutyCycle(0)
    elif speed < 0:
        motor_pwm1.ChangeDutyCycle(0)
        motor_pwm2.ChangeDutyCycle(abs(speed))
    else:
        motor_pwm1.ChangeDutyCycle(0)
        motor_pwm2.ChangeDutyCycle(0)

def accosta_destra(speed):
    motorsx_pwm1.ChangeDutyCycle(speed-1)
    motorsx_pwm2.ChangeDutyCycle(0)
    motordx_pwm1.ChangeDutyCycle(speed-10)
    motordx_pwm2.ChangeDutyCycle(0)

def accosta_sinistra(speed):
    motorsx_pwm1.ChangeDutyCycle(speed-10)
    motorsx_pwm2.ChangeDutyCycle(0)
    motordx_pwm1.ChangeDutyCycle(speed-1)
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
    motorsx_pwm1.ChangeDutyCycle(speed)
    motorsx_pwm2.ChangeDutyCycle(0)
    motordx_pwm1.ChangeDutyCycle(speed)
    motordx_pwm2.ChangeDutyCycle(0)

def indietro(speed):
    motorsx_pwm2.ChangeDutyCycle(speed)
    motorsx_pwm1.ChangeDutyCycle(0)
    motordx_pwm2.ChangeDutyCycle(speed)
    motordx_pwm1.ChangeDutyCycle(0)
    
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

# Funzione principale che legge i tasti
if __name__ == "__main__":
    try:
        while True:
            if keyboard.is_pressed('up'):  # Freccia su per andare avanti
                avanti(vel)
            elif keyboard.is_pressed('down'):  # Freccia giù per andare indietro
                indietro(vel)
            elif keyboard.is_pressed('left'):  # Freccia sinistra per accostarsi a sinistra
                svolta_sinistra(vel)
            elif keyboard.is_pressed('right'):  # Freccia destra per accostarsi a destra
                svolta_destra(vel)
            else:
                stop()  # Se nessun tasto è premuto, fermiamo i motori

            time.sleep(0.1)  # Pausa per evitare un uso eccessivo della CPU

    except KeyboardInterrupt:
        chiudi()
