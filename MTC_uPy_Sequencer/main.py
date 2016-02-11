from pyb import UART
from pwm import ledpwm
import gc


class sequence():

    def __init__(self):
        self.dataTxt = open("sequence.txt")
        self.sequence = self.getSequence(self.dataTxt)

    def getStep(self, stepNumber):
        self.dataTxt.seek(self.sequence[stepNumber])
        return self.dataTxt.readline()

    def getSequence(self, sequenceFile):

        def strIsInt(string):
            try:
              int(string)
              return True
            except:
              return False

        sequence = {}
        seqStep = 0
        lastLine = 0
        # Index the seqence so that a line can be recalled very fast
        for line in sequenceFile:
            if strIsInt(line[0]): # If first charachter is an int it means it is a step
                sequence[seqStep] = lastLine
                lastLine = self.dataTxt.tell()
                seqStep += 1
            elif sequence == {}: # caputre line before first line
                lastLine = self.dataTxt.tell()
        return sequence

seq_man = sequence()
sequenceLen = len(seq_man.sequence)


GreenF = 150
step = 0

pin = [

  	ledpwm('Y1',8,1,GreenF),
	ledpwm('Y6',1,1,GreenF), #inv
 	ledpwm('Y2',8,2,GreenF),
 	ledpwm('Y12',1,3,GreenF),
 	ledpwm('X3',9,1,GreenF),
 	ledpwm('X6',0,0,GreenF),
	ledpwm('X5',0,0,GreenF),
 	ledpwm('Y11',1,2,GreenF) #inv
]


def allPWM(value):
	for led in pin:
		led.pwm(value)

allPWM(0)





class MTC():

  def __init__(self):
      self.clock = {'frames':0, 'seconds':0, 'mins':0, 'hours':0, 'mode':0}
      self.frame_count = 1
      self.message = [0] * 8
      self.uart1 = UART(1)
      self.uart1.init(31250, parity=None, stop=1)

  def saveClock(self):
      self.clock['frames'] = (self.message[1] << 4) + self.message[0] # 2 half bytes 000f ffff
      self.clock['seconds'] = (self.message[3] << 4) + self.message[2] # 2 half bytes 00ss ssss
      self.clock['mins'] =  (self.message[5] << 4) + self.message[4] # 2 half bytes 00mm mmmm
      self.clock['hours'] = ((self.message[7] & 1) << 4) + self.message[6] # 2 half bytes 0rrh hhhh the msb has to be masked as it contains the mode
      self.clock['mode'] = ((self.message[7] & 6) >> 1) # get the fps mode by masking 0rrh with 0110 (6)

  def read(self):

      data = self.uart1.read(1)

      if data != None:
          if ord(data) == 241:              # if Byte for quater frame message
              mes = int(ord(self.uart1.read(1)))        # Read next byte
              piece = mes >> 4             # Get which part of the message it is (e.g seconds mins)

              if piece < 7:
                self.message[piece] = mes & 15    # store message using '&' to mask the bit type


              if piece == 7 or self.frame_count == 4:

                  self.saveClock()

                  if self.frame_count == 4:
                      self.message[0] -= 1
                  else:
                      self.message[0] += 1

                  if self.frame_count >= 8:
                      self.frame_count = 1

                  self.frame_count += 1

      return self.clock




                  #print("[%d] %d:%d:%d  Mode %d" % (frames, seconds, mins, hours, mode))





mtc = MTC()

last_total_frames = 0

togg = True

counter = pyb.Timer(2)

setTimer = 1 / (1.8 / 4)

counter.init(freq = setTimer)

sub_step = False
subcount = 1

def sub_state():
  global sub_step
  sub_step = True

counter.callback(lambda o: sub_state())

while True:


  clock = mtc.read()

  total_frames = (((((clock['hours'] * 60) + clock['mins']) * 60) + clock['seconds']) * 30 ) + clock['frames']

  if clock['frames'] <= 0:
      pass #pin[0].pwm(100)
  else: pin[0].pwm(0)



  if (total_frames % 54) == 0 and total_frames != last_total_frames:
      counter.counter(0)
      last_total_frames = total_frames

      step = int(total_frames/54)

      #pin[1].pwm(100)

      subcount = 1

      if step < sequenceLen:
          print('[%d] %s' % (step, seq_man.getStep(step)) )
      else:
          print("EOS")

  else:
      #pin[1].pwm(0)

      if sub_step:

           pin[2].pwm(100)
           print(subcount)
           subcount+=1
           sub_step = False
           print('[%d] %s' % (subcount, seq_man.getStep(subcount)) )

      else:
           pin[2].pwm(0)






  line_number = 0






              #print(message[1] << 4, message[0])





# while True:
#   data = uart1.read(1)
#   if data != None:
#
#       if ord(data) == 241:
#         mes = uart1.read(1)
#         if ord(mes) == 118:
#             print(message)
#             count = 0
#         message[count] = ord(mes) & 15
#         count += 1
#

          #print(data,ord())
