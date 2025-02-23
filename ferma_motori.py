from rpi_hardware_pwm import HardwarePWM
pwm = HardwarePWM(pwm_channel=0, hz=50000, chip=0)
pwm2 = HardwarePWM(pwm_channel=1, hz=50000, chip=0)

pwm.stop()
pwm2.stop()