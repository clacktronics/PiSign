#!/usr/bin/env

from time import sleep
import subprocess,dbus,getpass,os,signal,random
from re import match, search

class media():
	def __init__(self,media,**kwargs):
		self.media = media

		try:
			#self.nick = match('[0-9A-Za-z]*', media).group(0)
			self.nick = int(random.random() * 1000)

		except:
			print 'error filename must start with  numbers or letters'
		
		self.cmd = ['omxplayer']
		self.dbusname = 'org.mpris.MediaPlayer2.OMX%s' % self.nick
		self.cmd.extend(['--no-osd','--dbus_name',self.dbusname])

		for var,property in kwargs.iteritems():
			pass
			self.cmd.extend(['--%s' % (var), property])
		if '-o' not in self.cmd:
			self.cmd.extend(['-o','both'])
		self.cmd.append(media)

	def cue(self):

		print self.cmd
		devnull = open(os.devnull, 'wb')
		self.player = subprocess.Popen(self.cmd,shell=False)
		self.pid =  self.player.pid

		done,retry = 0,0
		while done == 0:
			try:
				dbusfile = '/tmp/omxplayerdbus.%s' % getpass.getuser() # open up the dbus file, it ends in user name	
				with open(dbusfile, 'r+') as f:
					omxplayerdbus = f.read().strip() # get the dbus and load it into dbus module
				bus = dbus.bus.BusConnection(omxplayerdbus)
				self.object = bus.get_object(self.dbusname,'/org/mpris/MediaPlayer2', introspect=False)
				# PlayerProp is for finding out info about current stream and some volume control
				self.PlayerProp = dbus.Interface(self.object,'org.freedesktop.DBus.Properties') 
        			# PlaterInter is the interface to control the video ( e.g seek, pause etc etc )
				self.PlayerInter = dbus.Interface(self.object,'org.mpris.MediaPlayer2.Player')
				self.pause()
				done = 1
			except Exception,e: # try 50 times until it connects
				retry+=1
				if retry >= 50:
					print 'fail'
					print str(e)
					done = 1	



	# Timeline actions with pause and seek
	def pause(self):
		self.PlayerInter.Pause()

	def paused(self):
		if self.PlayerProp.PlaybackStatus() != "Paused":
			self.pause()
	def unpaused(self):
		if self.PlayerProp.PlaybackStatus() == "Paused":
			self.pause()

	def quit(self):
		print self.PlayerProp.CanQuit()
		self.object.Quit()
		#self.player.kill()
		#self.player.terminate()
		try: os.kill(self.pid, 0)
		except OSError: print 'OSerr'
		else: print 'its fucking running'
		os.kill(self.pid, signal.SIGKILL)
	# Audio actions
	
	def volume(self,level):
		self.PlayerProp.Volume(dbus.Double(level))

	def fade(self,direction,duration,*args):
		stepSleep = duration / 100.
		for i in range(101):
			if direction == 'in':
				vol = i / 100.
			if direction == 'out':
				vol = (100 - i) / 100.
			self.volume(vol)
			sleep(stepSleep)
			print vol
		if 'kill' in args:
			self.quit()

	def unmute(self):
		self.PlayerProp.Unmute()
	
	# Video actions

	def resize(self,x1,y1,x2,y2):
		pos = '%s %s %s %s' % (str(x1),str(y1),str(x2),str(y2))
		self.PlayerInter.VideoPos(dbus.ObjectPath('/not/used'),dbus.String(pos))
		print 'set pos to ' + pos

	def getRes(self):

		# Use Raspberry Pi's built in screen program to get resolution
		tvservice = subprocess.Popen(['tvservice','-s'], stdout=subprocess.PIPE)
		tvstatus, err = tvservice.communicate()
		screenres = search(' ([0-9]*)x([0-9]*) ',tvstatus)
		self.screenX,self.screenY = int(screenres.group(1)), int(screenres.group(2))

		# Get movies info from another instance of omx
		omx = subprocess.Popen(['omxplayer','-i', self.media], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out,err = omx.communicate()
		vidres = search(' ([0-9]*)x([0-9]*) ',err)
		self.videoX,self.videoY = int(vidres.group(1)),int(vidres.group(2))
		
		#print 'screen %dx%d , video%dx%d' % (self.screenX,self.screenY,self.videoX,self.videoY)

	def fullscreen(self,type):
		# fit and fill are not exact due to rounding floats
		self.getRes()

		sratio = self.screenX / float(self.screenY)
		vratio = self.videoX / float(self.videoY)

		if type == "fit":
			if sratio == vratio:

				x1,y1,x2,y2 = 0,0,self.screenX,self.screenY

			if sratio > vratio:

				xwidth = self.videoX * (self.screenY / float(self.videoY))
				xoffset = (self.screenX - xwidth) / 2
				x1 = int(xoffset)
				x2 = int(self.screenX - xoffset)

				x1,y1,x2,y2 = x1,0,x2,self.screenY

			if sratio < vratio:

				vheight = self.videoY * (self.screenX / float(self.videoX))
				voffset = (self.screenY - vheight) / 2
				y1 = int(voffset)
				y2 = int(self.screenY - voffset)

				x1,y1,x2,y2 = 0,y1self.screenX,y2

		elif type == "fill":
			if sratio == vratio:

				x1,y1,x2,y2 = 0,0,self.screenX,self.screenY

			elif sratio > vratio:
				# calculate overflow top and bottom
				vheight = self.videoY * (self.screenX / float(self.videoX))
				voffset = (vheight - self.screenY) / 2
				y1 = int(0 - voffset)
				y2 = int(self.screenY + voffset)

				x1,y1,x2,y2 = 0,y1,self.screenX,y2
			
			elif sratio < vratio:
				# Calculate overflow on sides
				xwidth = self.videoX * (self.screenY / float(self.videoY))
				xoffset = (xwidth - self.screenX) / 2
				x1 = int(0 - xoffset)
				x2 = int(self.screenX + xoffset)

				x1,y1,x2,y2 = x1,0,x2,self.screenY

		elif type == "stretch":

			x1,y1,x2,y2 = 0,0,self.screenX,self.screenY

		elif type == "actual":
			x1 = (self.screenX - self.videoX) / 2
			x2 = x1 + self.videoX
			y1 = (self.screenY - self.videoY) / 2
			y2 = y1 + self.videoY
		else: 
			print "Sorry, command not understood, use 'fit','fill'.'actual' or 'stretch'"
			self.fullscreen('fit')
		
		self.resize(x1,y1,x2,y2)
		self.position = [x1,y1,x2,y2]
		

	def alpha(self,alpha):
		self.PlayerInter.SetAlpha(dbus.ObjectPath('/not/used'),dbus.Int64(alpha))
		#print 'Alpha  set to %s' % alpha
	
	def wipe(self,type,duration,*args):
		x1,y1,x2,y2 = self.position
		if 'left' in args:
			startPoint = self.position[2]
			endPoint = 0
			mediaDim =  self.position[2] - self.position[0]
			if duration > 5:
				step = -1 
				stepSpeed = duration / startPoint

			else: 
				step = -50
				stepSpeed = duration / (startPoint / 50 )
			xmod = step
			ymod = 0
		elif 'right' in args:
			startPoint = self.position[0]
			endPoint = self.screenX
			
		# shift(left/right,up/down)
		if type == "shift":
				for i in range(startPoint,endPoint+1,step):
					x1 = x1 + xmod
					x2 = x2 + xmod
					y1 = y1 + ymod
					y2 = y2 + ymod
					if x1 < 0 and x2 < 0:
						break
					if y1 < 0 and y2 < 0:
						break
					self.resize(x1,y1,x2,y2)
					sleep(stepSpeed)
			
		# fold(left/right/up/down)
		# shrink to point
		# shrink to line
		# expand to mass
		# expand widt
		
	def animate(self,type):
		pass
		# ping pong
		# Spiral grow
		# shudder
		# flicker

	def dissolve(self,direction,duration,*args):
		stepSleep = duration / 255
		if direction=="in":
			for i in range(256):
				self.alpha(i)
				sleep(stepSleep)
		elif direction=="out":
			for i in range(256):
				self.alpha(i)
				sleep(stepSleep)
		else:
			print "sorry, invalid command direction should be 'in' or 'out'"
		if "kill" in args:
			self.quit()
		
