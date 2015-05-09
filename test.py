from subprocess import call
from time import sleep
from media_modules import omxplayer
vid1 = omxplayer.media('stvincent.mp4', win = '-640,0,640,720')

vid1.cue()
sleep(5)
vid1.pause()
call(['reset'])
