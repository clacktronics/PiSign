from subprocess import call
from time import sleep
from media_modules import omxplayer
import subprocess

count = 1
while True:
	vid1 = omxplayer.media('future.mp4', layer = '2')
	vid1.cue()
	try: 
		vid4.quit()
	except Exception,e:
		print str(e)
	vid1.unpaused()
	sleep(2)
	vid3 = omxplayer.media('bishop.mp4', layer = '3')
	vid3.cue()
	vid1.quit()
	vid3.unpaused()
	sleep(2)
	print count
	count += 1
	vid4 = omxplayer.media('stvincent.mp4', layer = '2')
	vid4.cue()
	vid3.quit()
	vid4.unpaused()
	sleep(2)
	print count
	count+= 1
