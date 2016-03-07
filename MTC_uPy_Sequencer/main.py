from pyb import UART, micros
from pwm import ledpwm
from time import sleep
from MTC import MTC
from seq_reader import sequence

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

def setPWM(input):
    assert len(input) == 8

    for i,val in enumerate(input):
        out = val * 10
        pin[i].pwm(out)

allPWM(0)

if __name__ == "__main__":
    mtc = MTC()

    def frame_to_ms(frame):
        mins = ((frame['hours'] * 60) + frame['mins'])
        seconds = (mins * 60) + frame['seconds']
        frames = (seconds * 25) + frame['frames']
        milliseconds = frames * 40
        return milliseconds

    def frame_to_secs(frame):
        mins = ((frame['hours'] * 60) + frame['mins'])
        seconds = (mins * 60) + frame['seconds']
        frames = (seconds * 25) + frame['frames']
        milliseconds = frames * 40
        return milliseconds



    sequence = sequence()
    print(sequence.getStep(100))


    i = 0


    start = pyb.millis()
    difference = 0


    last = 0
    last2 = 0
    m = 1

    for i in range(sequence.length-4,sequence.length):
        print(i, sequence.getStep(i))

    #while True:


        # elapsed = (pyb.millis() - start) + difference
        #
        # #print mtc.getMs()
        # #print(elapsed - last)
        # #last = elapsed



        # if elapsed % 225 == 0 and elapsed != 0 and last != elapsed:
        #     i = int(elapsed / 225)
        #     # if i < sequence.length:
        #     #     print('[%d] %s' % (i, sequence.getStep(i).strip(' ')))
        #     # else:
        #     #     print('End of sequence')
        #     #out = [int(x) for x in sequence.getStep(i).strip().split(' ')]
        #     print(i,sequence.getStep(i))
        #     #setPWM(out)
        #
        #
        #     #print(pyb.millis()-last2)
        #     last2=pyb.millis()
        #
        #     m += 1
        #     if m == 20:
        #         difference += int((mtc.getMs() - elapsed)/100)*100
        #         m = 1
        #     #print(elapsed, mtc.readFrame())
        #     #print(int(mtc.getMs()/1000),int(elapsed/1000),difference)
        #     last = elapsed
