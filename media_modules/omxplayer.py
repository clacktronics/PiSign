#!/usr/bin/env

import subprocess
from re import match

class media():
	def __init__(self,media,**kwargs):
		try:
			self.nick = match('[0-9A-Za-z]*', media).group(0)
		except:
			print 'error filename must start with  numbers or letters'
		
		self.cmd = ['omxplayer']
		self.cmd.extend(['--dbus_name','org.mpris.MediaPlayer2.OMX%s' % self.nick])

		for var,property in kwargs.iteritems():
			pass
			self.cmd.extend(['--%s' % (var), property])
		if '-o' not in self.cmd:
			self.cmd.extend(['-o','both'])
		self.cmd.append(media)
			

	def load(self):
		print self.cmd
		subprocess.Popen(self.cmd)
