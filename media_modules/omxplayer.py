#!/usr/bin/env

from time import sleep
import subprocess,dbus,getpass,os
from re import match

class media():
	def __init__(self,media,**kwargs):
		try:
			self.nick = match('[0-9A-Za-z]*', media).group(0)
		except:
			print 'error filename must start with  numbers or letters'
		
		self.cmd = ['omxplayer']
		self.dbusname = 'org.mpris.MediaPlayer2.OMX%s' % self.nick
		self.cmd.extend(['--dbus_name',self.dbusname])

		for var,property in kwargs.iteritems():
			pass
			self.cmd.extend(['--%s' % (var), property])
		if '-o' not in self.cmd:
			self.cmd.extend(['-o','both'])
		self.cmd.append(media)

	def cue(self):

		print self.cmd
		devnull = open(os.devnull, 'wb')
		self.player = subprocess.Popen(self.cmd, stdout = devnull)

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
				self.PlayerInter.Action(dbus.Int32("16"))
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

	def paused():
		pass
	def unpaused():
		pass
	def quit(self):
		self.object.Quit()

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
	
	# Visual Video actions

	def resize(self,x1,y1,x2,y2):
		pos = '%s %s %s %s' % (str(x1),str(y1),str(x2),str(y2))
		self.PlayerInter.VideoPos(dbus.ObjectPath('/not/used'),dbus.String(pos))
		print 'set pos to ' + pos

	def alpha(self,alpha):
		self.PlayerInter.SetAlpha(dbus.ObjectPath('/not/used'),dbus.Int64(alpha))
		#print 'Alpha  set to %s' % alpha
	

		
		
