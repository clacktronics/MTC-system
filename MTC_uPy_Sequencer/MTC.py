from pyb import UART

class MTC():

  def __init__(self):
      self.clock = {'frames':0, 'seconds':0, 'mins':0, 'hours':0, 'mode':0}
      self.frame_count = 1
      self.uart1 = UART(1)

      self.message = [-1] * 8
      self.uart1.init(31250, parity=None, stop=1,read_buf_len=1)
      print(dir(self.uart1))

  def saveClock(self):
      self.clock['frames'] = (self.message[1] << 4) + self.message[0] # 2 half bytes 000f ffff
      self.clock['seconds'] = (self.message[3] << 4) + self.message[2] # 2 half bytes 00ss ssss
      self.clock['mins'] =  (self.message[5] << 4) + self.message[4] # 2 half bytes 00mm mmmm
      self.clock['hours'] = ((self.message[7] & 1) << 4) + self.message[6] # 2 half bytes 0rrh hhhh the msb has to be masked as it contains the mode
      self.clock['mode'] = ((self.message[7] & 6) >> 1) # get the fps mode by masking 0rrh with 0110 (6)

  def getMs(self):

      self.readFrame()
      mins = ((self.clock['hours'] * 60) + self.clock['mins'])
      seconds = (mins * 60) + self.clock['seconds']
      frames = (seconds * 25) + self.clock['frames']
      milliseconds = frames * 40
      return milliseconds

  def readFrame(self):


      indice = 0
      self.message = [-1] * 8

      while True:

          data = self.uart1.read(1)

          if data != None:

              if ord(data) == 241:              # if Byte for quater frame message

                  try: mes = int(ord(self.uart1.read(1)))        # Read next byte
                  except: continue

                  piece = mes >> 4             # Get which part of the message it is (e.g seconds mins)

                  if piece == indice:
                      self.message[piece] = mes & 15    # store message using '&' to mask the bit type
                      indice += 1

          if indice > 7:
              self.saveClock()
              break

      #self.uart1.deinit()
      return self.clock
