from subprocess import call
from time import sleep
from media_modules import omxplayer
vid1 = omxplayer.media('future.mp4',vol = '-6000', layer = '2')
 
vid1.cue()

sleep(1)

vid1.pause()
while True:
#	vid1.fullscreen('stretch')
	sleep(5)
	vid1.fullscreen('actual')
#	sleep(5)
#	vid1.fullscreen('fill')
	sleep(5)
	vid1.fullscreen('fit')
	sleep(5)
