from omxplayer import OMXPlayer
from MTC import MTC


if __name__ == "__main__":

    from time import sleep
    import threading

    player = OMXPlayer('timer.mp4')
    mtc = MTC()
    player.play()

    def get_mtc():
        while True:
            mtc.readFrame()

    mtc_time = threading.Thread(target=get_mtc)
    mtc_time.start()
    speed = 0
    lastm, lastp = 0, 0

    sleep(1)
    av = []

    try:
      while True:
        player_pos = player.position()
        mtc_pos = mtc.getS()
        difference = player_pos - mtc_pos
        pl_dev = player_pos - lastp
        mt_dev = mtc_pos - lastm

        av.append(player_pos)
        if len(av) > 10:
            av.pop(0)
        pl_av = sum(av)/len(av)

        print "Video: %.2f / %.2f (%.2f) MTC: %.2f" % (player_pos, pl_av, pl_dev, mtc_pos)

        # print "%3f %6f" % (pl_dev, mt_dev)
        # print sum(av)/len(av)

        if difference > 6 or difference < -6:
            print difference
             #player.seek((difference*1000000)*-1)


        sleep(0.1)


            # pause_pos = mtc.getS()+2
            # player.set_position(pause_pos)
            # print "seeking to %f" % (pause_pos / 60)
            # while mtc.getS() < (pause_pos): pass
            # player.play()

        lastm = mtc_pos
        lastp = player_pos

        # elif difference > 1 and speed == 0:
        #     player.action(1)
        #     speed = -1
        # elif difference < -1 and speed == 0:
        #     player.action(2)
        #     speed = 1
        # else:
        #     if speed == 1:
        #         player.action(1)
        #     elif speed == -1:
        #         player.action(2)
        #     speed = 0


    except KeyboardInterrupt:
    	player.quit()
