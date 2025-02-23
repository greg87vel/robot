import RPi.GPIO as GPIO
import time

# Definizione dei pin per i motori
MOTOR1_IN1 = 21  # GPIO per direzione motore 1
MOTOR1_IN2 = 20  # GPIO per direzione motore 1
MOTOR2_IN1 = 19  # GPIO per direzione motore 2
MOTOR2_IN2 = 26  # GPIO per direzione motore 2

# Frequenza PWM
PWM_FREQ =30000  # Hz

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup([MOTOR1_IN1, MOTOR1_IN2, MOTOR2_IN1, MOTOR2_IN2], GPIO.OUT)

# Creazione degli oggetti PWM
motor1_pwm1 = GPIO.PWM(MOTOR1_IN1, PWM_FREQ)
motor1_pwm2 = GPIO.PWM(MOTOR1_IN2, PWM_FREQ)
motor2_pwm1 = GPIO.PWM(MOTOR2_IN1, PWM_FREQ)
motor2_pwm2 = GPIO.PWM(MOTOR2_IN2, PWM_FREQ)

# Avvio dei PWM con duty cycle a 0 (fermi)
motor1_pwm1.start(0)
motor1_pwm2.start(0)
motor2_pwm1.start(0)
motor2_pwm2.start(0)

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

def avanti(speed):
    motor1_pwm1.ChangeDutyCycle(speed)
    motor1_pwm2.ChangeDutyCycle(0)
    motor2_pwm1.ChangeDutyCycle(speed)
    motor2_pwm2.ChangeDutyCycle(0)

def indietro(speed):
    motor1_pwm2.ChangeDutyCycle(speed)
    motor1_pwm1.ChangeDutyCycle(0)
    motor2_pwm2.ChangeDutyCycle(speed)
    motor2_pwm1.ChangeDutyCycle(0)
    
def stop():
    motor1_pwm2.ChangeDutyCycle(0)
    motor1_pwm1.ChangeDutyCycle(0)
    motor2_pwm2.ChangeDutyCycle(0)
    motor2_pwm1.ChangeDutyCycle(0)

def chiudi():
    motor1_pwm1.stop()
    motor1_pwm2.stop()
    motor2_pwm1.stop()
    motor2_pwm2.stop()
    GPIO.cleanup()
    print("Chiusura e pulizia GPIO.")
    

if __name__ == "__main__":
    
    try:
        while True:
            sx = (motor1_pwm1, motor1_pwm2)
            dx = (motor2_pwm1, motor2_pwm2)
            set_motor_speed(*sx, 100)
            set_motor_speed(*dx, 100)
    except KeyboardInterrupt:
        chiudi()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
