#!/usr/bin/env

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
		player = subprocess.Popen(self.cmd, stdout = devnull)


		done,retry = 0,0
		while done == 0:
			try:
				dbusfile = '/tmp/omxplayerdbus.%s' % getpass.getuser()	
				with open(dbusfile, 'r+') as f:
					omxplayerdbus = f.read().strip()
				bus = dbus.bus.BusConnection(omxplayerdbus)
				object = bus.get_object(self.dbusname,'/org/mpris/MediaPlayer2', introspect=False)
				self.dbusIfaceProp = dbus.Interface(object,'org.freedesktop.DBus.Properties')
        			self.dbusIfaceKey = dbus.Interface(object,'org.mpris.MediaPlayer2.Player')
				self.dbusIfaceKey.Action(dbus.Int32("16"))
				done = 1
			except Exception,e:
				retry+=1
				if retry >= 50:
					print 'fail'
					print str(e)
					done = 1	



	def pause(self):
		self.dbusIfaceKey.Action(dbus.Int32("16"))
