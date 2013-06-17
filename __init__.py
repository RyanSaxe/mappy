def time_sample(sample,times,*args):
  if type(times[0]) == str:
		from dateutil import parser
		times = [parser.parse(x) for x in times]
	if len(sample) == 1:
		amount = 1
	else:
		amount = int(sample[1:])
	sampler = sample[0]
	count = 1
	if sampler in 'YMDhms':
		sampled = [[times[0]]]
		for array in args:
			sampled.append([array[0]])
		if sampler in 'YMD':
			from datetime import datetime as DateTime
			for time in times[1:]:
				good = False
				yt = time.year - sampled[0][-1].year
				mt = time.month - sampled[0][-1].month
				dt = DateTime.date(time) - DateTime.date(sampled[0][-1])
				if sampler == 'Y':
					if yt >= amount:
						good = True
				elif sampler == 'M':
					if yt > 0:
						mt = (12 * amount + time.month) - sampled[0][-1].month
					if mt >= amount:
						good = True
				else:
					if dt.days >= amount:
						good = True
					#multiplyer = timedelta(days=amount).total_seconds()
				if good:
					sampled[0].append(time)
					mini_count = 1
					for array in args:
						sampled[mini_count].append(array[count])
						mini_count += 1
				count += 1
		else:
			from datetime import timedelta
			if sampler =='h':
				multiplyer = timedelta(hours=amount).total_seconds()
			elif sampler == 'm':
				multiplyer = timedelta(minutes=amount).total_seconds()
			else:
				multiplyer = float(amount)
			for time in times[1:]:
				td = time - sampled[0][-1]
				if td.total_seconds() > multiplyer:
					sampled[0].append(time)
					mini_count = 1
					for array in args:
						sampled[mini_count].append(array[count])
						mini_count += 1
				else:
					pass
				count += 1
	else:
		print 'Your sample type was not an option, so your original inputs were returned'
		sampled = [times,args]
	return sampled
def common_finder(*args):
	import collections
	z = zip(*args)
	#print z
	places = [','.join(x) for x in z]
	answer = collections.Counter(places).most_common(1)
	return answer[0][0]
def between_times(times,item,by='start'):
	new_times = []
	for time in times:
		if by == 'start':
			if time >= item:
				answer = times.index(time)
				break
		else:
			if time >= item:
				answer = times.index(time) - 1
				break
	return answer
def url_maker(latitudes,longitudes,times=None,color='red',label=' ',zoom=12,center=None,start=None,end=None,by=None,size='600x300'):
	urls = []	
	import datetime
	latitudes,longitudes,times = list(latitudes),list(longitudes),list(times)
	if isinstance(times[0],str) or isinstance(times[0],datetime.datetime):
		#print 1
		from dateutil import parser
		if isinstance(times[0],str):
			times = [parser.parse(x) for x in times]
		if isinstance(start,str):
			startindex = parser.parse(start)
		else:
			startindex = start
		if isinstance(end,str):
			endindex = parser.parse(end)
		else:
			endindex = end
		#print endindex,startindex
		if isinstance(startindex,datetime.datetime):
			startpos = between_times(times,startindex,by='start')
		elif isinstance(startindex,int):
			if isinstance(endindex,datetime.datetime):
				startpos = between_times(times,endindex,by='end') - start
			else:
				startpos = start
		else:
			startpos = start
		if isinstance(endindex,datetime.datetime):
			endpos = between_times(times,endindex,by='end')
		elif isinstance(endindex,int):
			if isinstance(startindex,datetime.datetime):
				endpos = between_times(times,startindex,by='start') + end
			else:
				endpos = end
		else:
			endpos = end
	else:
		#print 2
		startpos = start
		endpos = end
		times = range(1,len(latitudes) + 1)
		if isinstance(start,int):
			startpos = start
		else:
			startpos = None
		if isinstance(end,int):
			endpos = end
		else:
			endpos = None
	if isinstance(by,str):
		lat,lon,t = latitudes[startpos:endpos],latitudes[startpos:endpos],times[startpos:endpos]
		#print lat
		t,lats,lons = time_sample(by,t,lat,lon)
	elif isinstance(by,int):
		lats,lons,t = latitudes[startpos:endpos:by],latitudes[startpos:endpos:by],times[startpos:endpos:by]
	else:
		lats,lons,t= latitudes[startpos:endpos],latitudes[startpos:endpos],times[startpos:endpos]
	#print t
	#print len(t)
	if center == None:
		latit = [str(i) for i in lats]
		longi = [str(i) for i in lons]
		center = '&center=' + common_finder(latit,longi)
	else:
		center = '&center=' + '+'.join(center.split())
	zoom = '&zoom=' + str(zoom)
	for i in range(len(lats)):
		#label = str(i)
		x,y = str(lats[i]),str(lons[i])
		marker = '&markers=color:' + color + '%7Clabel:' + label + '%7C' + x + ',' + y
		url = 'http://maps.googleapis.com/maps/api/staticmap?maptype=roadmap&size=' + size + zoom + center + marker + '&sensor=true'
		urls.append(url)
		#print i
	return urls,t
def get_single_map(folder,name,latitude,longitude,label=' ',color='red',zoom=12,center=None,size='600x300'):
	from urllib import urlretrieve
	if folder[-1] != '/':
		folder = folder + '/'
	print folder
	point = str(latitude) + "," + str(longitude)
	print point
	file_name = folder + name + '.jpg'
	if center == None:
		center = ''
	else:
		center = '&center=' + '+'.join(center.split())
	print center
	zoom = '&zoom=' + str(zoom)
	marker = '&markers=color:' + color + '%7Clabel:' + label + '%7C' + point
	url = 'http://maps.googleapis.com/maps/api/staticmap?maptype=roadmap&size=' + size + zoom + center + marker + '&sensor=true'
	print url
	urlretrieve(url,file_name)
def get_multiple_map(folder,name,latitudes,longitudes,labels=None,colors=None,zoom=12,center=None,size='600x300'):
	from urllib import urlretrieve
	if folder[-1] != '/':
		folder = folder + '/'
	file_name = folder + name + '.jpg'
	markers = []
	places = zip(latitudes,longitudes)
	final_size = len(places)
	if labels == None:
		label = [' '] * final_size
	else:
		if final_size - len(labels) < 0:
			label = labels[:final_size]
		else:
			label = labels + ['?'] * (final_size - len(labels))
	if colors == None:
		color = ['black'] * final_size
	else:
		if final_size - len(colors) < 0:
			color = colors[:final_size]
		else:
			color = colors + ['black'] * (final_size - len(colors))
	if center == None:
		center = ''
	else:
		center = '&center=' + '+'.join(center.split())
	zoom = '&zoom=' + str(zoom)
	count = 0
	for point in places:
		loc = str(point[0]) + ',' + str(point[1])
		marker = '&markers=color:' + color[count] + '%7Clabel:' + label[count] + '%7C' + loc
		markers.append(marker)
		count += 1
	url = 'http://maps.googleapis.com/maps/api/staticmap?maptype=roadmap&size=' + size + zoom + center + ''.join(markers) + '&sensor=true'
	urlretrieve(url,file_name)
def multi_mov(latitudes,longitudes,labels=None,colors=None,zoom=12,center=None,start=None,end=None,by=1,size='600x300'):
#	if 'pandas' in str(type(latitudes)):
#		latitudes = [list(i) for i in latitudes]
#	if 'pandas' in str(type(longitudes)):
#		longitudes = [list(i) for i in longitudes]
	cutlat = min([len(i) for i in latitudes])
	cutlon = min([len(i) for i in longitudes])
	latitudes = [s[:cutlat] for s in latitudes]
	longitudes = [s[:cutlon] for s in longitudes]
	urls = []
	points = zip(latitudes,longitudes)
	hold = []
	for point in points:
		x = [str(point[0][i]) + ',' + str(point[1][i]) for i in range(len(point[0]))]
		hold.append(x)
	#print len(hold)
	locs = zip(*hold)
	#print locs
	#print organize
	organize = locs[start:end:by]
	#print organize
	final_size = len(hold)
	if labels == None:
		label = [' '] * final_size
	else:
		if final_size - len(labels) < 0:
			label = labels[:final_size]
		else:
			label = labels + ['?'] * (final_size - len(labels))
	if colors == None:
		color = ['red'] * final_size
	else:
		if final_size - len(colors) < 0:
			color = colors[:final_size]
		else:
			color = colors + ['black'] * (final_size - len(colors))
	if center == None:
		center = ''
	else:
		center = '&center=' + '+'.join(center.split())
	zoom = '&zoom=' + str(zoom)
	for row in organize:
		markers = []
		count = 0
		for place in row:
			marker = '&markers=color:' + color[count] + '%7Clabel:' + label[count] + '%7C' + place
			markers.append(marker)
			count += 1
		url = 'http://maps.googleapis.com/maps/api/staticmap?maptype=roadmap&size=' + size + zoom + center + ''.join(markers) + '&sensor=true'
		urls.append(url)
	#print titles
	return urls
def movie_maker(urls,folder,name,_type='mov',loop=0,fps=5,titlebar=True,titles=None):
	from subprocess import call
	from urllib import urlretrieve
	from time import sleep
	from sys import platform as _platform
	if titles == None:
		titles = [str(i) for i in range(1,len(urls) + 1)]
	size2 = len(urls)
	size2 = len(str(size2))
	filler = '0' * size2
	count = 0
	for src in urls:
		try:
			title = titles[count]
		except:
			title = "Blank"
		count += 1
		s1 = len(str(count))
		s2 = size2 - s1
		#print src
		file_name = folder + filler[0:s2] + str(count) + '.png'
		#print file_name
		urlretrieve(src, file_name)
		if titlebar == True:
			call('convert %s -gravity North -background Gray -splice 0X18 -annotate +0+2 "%s" %s' % (file_name,title,file_name), shell=True)
		print str((count/float(len(urls)))*100) + ' percent done! only ' + str(len(urls) - count) + ' more pictures to download'
		sleep(3)
	frames = 30/float(fps)
	delay = 1000/fps
	final_name = folder + name + '.' + _type
	if _type.lower() == 'mov':
		call('convert -quality 100 ' + folder + '*.png ' + folder + 'test.mov', shell=True)
		command = "ffmpeg -i %s -filter:v 'setpts=%s*PTS' %s" % (folder + 'test.mov',str(frames),final_name)
		call(command,shell=True)
		if "darwin" in _platform:
			call('rm ' + folder + 'test.mov', shell=True)
		elif "linux" in _platform:
			call('DEL ' + folder + 'test.mov', shell=True)
		else:
			call('rm ' + folder + 'test.mov', shell=True)
	elif _type.lower() == 'gif':
		command = 'convert -set delay %s -loop %s ' % (str(delay),str(loop))
		call(command + folder + '*.png ' + final_name, shell=True)
	else:
		raise TypeError(
                "The only options for movie type are MOV and GIF."
            )
	#for mov
	if "darwin" in _platform:
		call('rm ' + folder + '*.png', shell=True)
	elif "linux" in _platform:
		call('DEL ' + folder + '*.png', shell=True)
	else:
		call('rm ' + folder + '*.png', shell=True)
def create_solo(folder,name,latitudes,longitudes,times=None,color='red',label=' ',zoom=12,center=None,start=None,end=None,by=None,size='600x300',_type='mov',loop=0,fps=5,titlebar=True):
	if folder[-1] != '/':
		folder = folder + '/'
	images,titles = url_maker(latitudes,longitudes,times=times,color=color,label=label,zoom=zoom,center=center,start=start,end=end,by=by,size=size)
	movie_maker(images,folder,name,_type=_type,loop=loop,fps=fps,titlebar=titlebar,titles=titles)
	print "Your movie has been created at " + folder + name + '.' + _type.lower()
def create_multi(folder,name,latitudes,longitudes,colors=None,labels=None,zoom=12,center=None,start=None,end=None,by=None,size='600x300',_type='mov',loop=0,fps=5,titlebar=True):
	if folder[-1] != '/':
		folder = folder + '/'
	images = multi_mov(latitudes,longitudes,colors=colors,labels=labels,zoom=zoom,center=center,start=start,end=end,by=by,size=size)
	movie_maker(images,folder,name,_type=_type,loop=loop,fps=fps,titlebar=titlebar)
	print "Your movie has been created at " + folder + name + '.' + _type.lower()
