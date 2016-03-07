from omxplayer import OMXPlayer
from MTC import MTC


if __name__ == "__main__":

    from time import sleep
    import threading

    player = OMXPlayer('chem.mp4', args=['--no-osd'])
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
    first_seek = True

    tol = 0.1

    try:
      while True:
        player_pos = player.position()
        mtc_pos = mtc.getS()
        difference = player_pos - mtc_pos
        pl_dev = player_pos - lastp
        mt_dev = mtc_pos - lastm
        print "(%.2f) %.2f %.2f" % (difference, mtc_pos, player_pos)

        # av.append(player_pos)
        # if len(av) > 10:
        #     av.pop(0)
        # pl_av = sum(av)/len(av)
        #
        # print "Video: %.2f / %.2f (%.2f) MTC: %.2f" % (player_pos, pl_av, pl_dev, mtc_pos)
        #
        # # print "%3f %6f" % (pl_dev, mt_dev)
        # # print sum(av)/len(av)
        #
        if difference > 5 or difference < -1:
            pause_pos = mtc.getS()+5
            player.set_position(pause_pos)
            print "seeking to %f" % (pause_pos / 60)
            player.pause()
            player_pos = player.position()
            while mtc.getS() < player_pos: pass
            player.play()

        # if difference > 0.2:
        #     player.pause()
        #     player.play()

        if difference > tol and speed == 0:
             player.action(1)
             speed = -1
        elif difference < -tol and speed == 0:
             player.action(2)
             speed = 1
        elif speed == -1 and difference < tol:
             player.action(2)
             speed = 0
        elif speed == 1 and difference > -tol:
             player.action(1)
             speed = 0

        lastm = mtc_pos
        lastp = player_pos


    except KeyboardInterrupt:
    	player.quit()
