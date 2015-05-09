from subprocess import call
from time import sleep
from media_modules import omxplayer
vid1 = omxplayer.media('stvincent.mp4', win = '-640,0,640,720',vol = '-6000')

vid1.cue()
sleep(5)
vid1.pause()
vid1.fade('in',10)
sleep(5)
vid1.fade('out',10,'kill')
#for i in range(256):
#	vid1.alpha(i)
#	sleep(.1)
