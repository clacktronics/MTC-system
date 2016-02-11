from time import sleep
import pyb

class ledpwm:
  def __init__(self,pin,timer,channel,freq):

    self.freq = freq
    self.timer = timer
    self.channel = channel
    self.pin = pin

    if pin == 'X5' or pin == 'X6':
      self.dac = pyb.DAC(pin)
      self.buf = bytearray(100)
      self.dac.write_timed(self.buf, freq * len(self.buf), mode=pyb.DAC.CIRCULAR)

    elif pin == 'P18':
      self.ch = pyb.LED(4)

    else:
      self.pinpwm = pyb.Pin(pin)
      timerset = pyb.Timer(self.timer, freq=self.freq)
      self.ch = timerset.channel(self.channel, pyb.Timer.PWM, pin=self.pinpwm)

  def pwm(self,PWM):
    if self.pin == 'X5' or self.pin == 'X6':
      b = self.buf # cache buf variable for speed
      pwm = PWM * len(b) // 100
      for i in range(len(b)):
        b[i] = 255 if i < pwm else 0
    elif self.pin == 'P18':
      PWM = self.map(PWM,0,100,0,256)
      self.ch.intensity(PWM)
    else:
      if self.pin in ('Y6','Y11','Y12'):
        PWM = int(self.map(PWM,0,100,100,0))
      self.ch.pulse_width_percent(PWM)

# Borrowed from Arduino
  def map(self,x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
