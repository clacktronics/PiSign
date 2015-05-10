from subprocess import call
from time import sleep
from media_modules import omxplayer

while True:
	vid1 = omxplayer.media('future.mp4', layer = '2')
	vid1.cue()
	try: 
		vid3.quit()
		del vid3
	except Exception,e:
		print str(e)
	vid1.unpaused()
	sleep(10)
	vid3 = omxplayer.media('bishop.mp4', layer = '3')
	vid3.cue()
	vid1.quit()
	del vid1
	vid3.unpaused()
	sleep(10)
