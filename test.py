from subprocess import call
from time import sleep
from media_modules import omxplayer
vid1 = omxplayer.media('stvincent.mp4',vol = '-6000', layer = '2')
vid2 = omxplayer.media('boy.mp4',vol = '-6000',layer = '1')
 
vid1.cue()
vid2.cue()

sleep(1)

vid1.pause()
vid2.pause()

vid1.fade('in',.5)

sleep(1)
x1 = 0
x2 = 1280
#for i in range(1281):
#	vid1.resize(x1,0,x2,720)
#	sleep(.01)
#	x1 += 1
#	x2 += 1
while True:
	for i in range(0,256,10):
		vid1.alpha(i)
vid1.fade('out',10,'kill')
