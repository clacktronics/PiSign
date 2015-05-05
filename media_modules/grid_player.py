import omxplayer,math,time

videos = ('vid.mp4','vid.mp4','vid.mp4','vid.mp4','vid.mp4','vid.mp4')
n_vids = len(videos)


divide = math.sqrt(n_vids)
if divide.is_integer():
	divider = int(divide)
else:
	divider = int(math.ceil(divide))

screenW = 1280
screenH = 720
screenX = screenW / divider
screenY = screenH / divider
	 
vid = {}
x1 = 0
y1 = 0
dcount = 0

for vno,vfile in enumerate(videos):
	dcount += 1
	x2 = x1 + screenX
	y2 = y1 + screenY
	
	dims = '%d %d %d %d' % (x1,y1,x2,y2)
	print vfile,dims
	vid[vno] = omxplayer.media(vfile,dims)
	vid[vno].load()

	x1 = x1 + screenX	

	if dcount == divider:
		x1 = 0
		y1 = y1 + screenY
		dcount = 0	

	time.sleep(5)
