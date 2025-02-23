from rpi_hardware_pwm import HardwarePWM
import time
import keyboard  # Modulo per rilevare la pressione di un tasto
from sonar import measure_distance

# Inizializzazione dei PWM per i due motori
motor1_in1 = HardwarePWM(pwm_channel=0, hz=5000, chip=0)  # GPIO 12
motor1_in2 = HardwarePWM(pwm_channel=1, hz=5000, chip=0)  # GPIO 18


# Avvio dei PWM
motor1_in1.start(0)
motor1_in2.start(0)


vel = int(input("Velocità di partenza: "))

def set_motor_speed(motor_in1, motor_in2, speed):
    if speed > 0:
        motor_in1.change_duty_cycle(speed)
        motor_in2.change_duty_cycle(0)
    elif speed < 0:
        motor_in1.change_duty_cycle(0)
        motor_in2.change_duty_cycle(-speed)
    else:
        motor_in1.change_duty_cycle(0)
        motor_in2.change_duty_cycle(0)

try:
    while True:
        # Accelerazione positiva
        for speed in range(vel, 101, 5):
            if keyboard.is_pressed("space"):  # Controllo se la barra spaziatrice è premuta
                raise KeyboardInterrupt  # Forzo l'interruzione del ciclo
            set_motor_speed(motor1_in1, motor1_in2, speed)
            print(f"Velocità: {speed}")
            time.sleep(0.2)
        
        for speed in range(100, vel, -5):
            if keyboard.is_pressed("space"):  # Controllo se la barra spaziatrice è premuta
                raise KeyboardInterrupt  # Forzo l'interruzione del ciclo
            set_motor_speed(motor1_in1, motor1_in2, speed)
            print(f"Velocità: {speed}")
            time.sleep(0.2)
        
        # Decelerazione e inversione
        for speed in range(-vel, -101, -5):
            if keyboard.is_pressed("space"):
                raise KeyboardInterrupt
            set_motor_speed(motor1_in1, motor1_in2, speed)
            print(f"Velocità: {speed}")
            time.sleep(0.2)
            
        for speed in range(-100, -vel, 5):
            if keyboard.is_pressed("space"):
                raise KeyboardInterrupt
            set_motor_speed(motor1_in1, motor1_in2, speed)
            print(f"Velocità: {speed}")
            time.sleep(0.2)
        
except KeyboardInterrupt:
    print("\nInterruzione rilevata, arresto motori...")
    motor1_in1.stop()
    motor1_in2.stop()
    print("Motori fermati, uscita dal programma.")
