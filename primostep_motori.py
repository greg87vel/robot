import RPi.GPIO as GPIO
import time
# Definizione dei pin
IN1 = 21
# Pin collegato a AIN1 del DRV8833
IN2 = 20 # Pin collegato a AIN2 del DRV8833
IN3 = 19
IN4 = 26
BUTTON_RIGHT = 22 # Pulsante per rotazione a destra
BUTTON_LEFT = 6
BUTTON_RIGHT1 = 24 # Pulsante per rotazione a destra
BUTTON_LEFT1 = 4
# Pulsante per rotazione a sinistra
# Configurazione GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(BUTTON_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_RIGHT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_LEFT1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def move_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
def move_right1():
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
def move_left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
def move_left1():
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
def stop_motor():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
def stop_motor1():
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
try:
    while True:
        right_pressed = GPIO.input(BUTTON_RIGHT) == GPIO.LOW
        left_pressed = GPIO.input(BUTTON_LEFT) == GPIO.LOW
        right_pressed1 = GPIO.input(BUTTON_RIGHT1) == GPIO.LOW
        left_pressed1 = GPIO.input(BUTTON_LEFT1) == GPIO.LOW
        if right_pressed and not left_pressed:
            move_right()
        elif left_pressed and not right_pressed:
            move_left()
        else:
            stop_motor()
            time.sleep(0.1)
        if right_pressed1 and not left_pressed1:
            move_right1()
        elif left_pressed1 and not right_pressed1:
            move_left1()
        
        else:
            stop_motor1()
            time.sleep(0.1)
        # Piccola pausa per evitare il rimbalzo dei pulsanti
except KeyboardInterrupt:
    print("Programma interrotto")
    GPIO.cleanup()