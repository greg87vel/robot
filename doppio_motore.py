import time
import os

PWM_CHIP = "/sys/class/pwm/pwmchip0"
PWM0 = PWM_CHIP + "/pwm0"  # GPIO12 (Ruota Sinistra - Avanti) e GPIO18 (Ruota Destra - Indietro)
PWM1 = PWM_CHIP + "/pwm1"  # GPIO19 (Ruota Sinistra - Indietro) e GPIO13 (Ruota Destra - Avanti)

def write_pwm(path, value):
    """Scrive un valore nei file sysfs del PWM, ignorando errori di file occupato."""
    try:
        with open(path, 'w') as f:
            f.write(str(value))
    except IOError as e:
        print(f"Errore: {e}")

def enable_pwm():
    """Abilita i canali PWM se non sono già attivati."""
    if not os.path.exists(PWM0):
        write_pwm(PWM_CHIP + "/export", 0)
    if not os.path.exists(PWM1):
        write_pwm(PWM_CHIP + "/export", 1)
    time.sleep(0.1)  # Attendi la creazione delle directory

def disable_pwm():
    """Disattiva le ruote e spegne i canali PWM."""
    write_pwm(PWM0 + "/enable", 0)
    write_pwm(PWM1 + "/enable", 0)
    write_pwm(PWM_CHIP + "/unexport", 0)
    write_pwm(PWM_CHIP + "/unexport", 1)

def set_wheels(direction, speed):
    """Imposta la direzione e velocità delle ruote."""
    frequency = 20000  # 20 kHz
    period_ns = int(1_000_000_000 / frequency)  # Converti Hz in nanosecondi
    duty_ns = int(abs(speed) * period_ns / 100)  # Duty cycle in ns
    duty_ns = max(0, min(duty_ns, period_ns))  # Assicura che duty_cycle sia valido

    if direction == "a":
        print(f"Ruote avanti: {speed}%")
        write_pwm(PWM0 + "/period", period_ns)
        write_pwm(PWM0 + "/duty_cycle", duty_ns)  # IN1 e IN3: PWM attivo
        write_pwm(PWM0 + "/enable", 1)

        write_pwm(PWM1 + "/enable", 0)  # IN2 e IN4 spenti

    elif direction == "i":
        print(f"Ruote indietro: {speed}%")
        write_pwm(PWM1 + "/period", period_ns)
        write_pwm(PWM1 + "/duty_cycle", duty_ns)  # IN2 e IN4: PWM attivo
        write_pwm(PWM1 + "/enable", 1)

        write_pwm(PWM0 + "/enable", 0)  # IN1 e IN3 spenti

    elif direction == "sx":
        print(f"Ruote girano a sinistra: {speed}%")
        write_pwm(PWM0 + "/period", period_ns)
        write_pwm(PWM0 + "/duty_cycle", duty_ns)  # IN1 e IN3 PWM attivo
        write_pwm(PWM0 + "/enable", 1)

        write_pwm(PWM1 + "/period", period_ns)
        write_pwm(PWM1 + "/duty_cycle", duty_ns)  # IN2 e IN4 PWM attivo
        write_pwm(PWM1 + "/enable", 1)

    elif direction == "dx":
        print(f"Ruote girano a destra: {speed}%")
        write_pwm(PWM1 + "/period", period_ns)
        write_pwm(PWM1 + "/duty_cycle", duty_ns)  # IN2 e IN4 PWM attivo
        write_pwm(PWM1 + "/enable", 1)

        write_pwm(PWM0 + "/period", period_ns)
        write_pwm(PWM0 + "/duty_cycle", duty_ns)  # IN1 e IN3 PWM attivo
        write_pwm(PWM0 + "/enable", 1)

    else:
        print("Ruote ferme")
        write_pwm(PWM0 + "/enable", 0)
        write_pwm(PWM1 + "/enable", 0)

if __name__ == "__main__":
    try:
        enable_pwm()

        while True:
            cmd = input("Comando: a (avanti), i (indietro), sx (sinistra), dx (destra), stop, q per uscire: ").lower()
            if cmd == 'q':
                break
            if cmd in ["a", "i", "sx", "dx", "stop"]:
                speed = 50  # Velocità fissa (puoi cambiarla dinamicamente)
                set_wheels(cmd, speed)
            else:
                print("Comando non valido.")

    except KeyboardInterrupt:
        print("\nSpegnimento motori...")
    finally:
        disable_pwm()
