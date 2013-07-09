MapPy
=====

This is a python module designed for taking GPS coordinates and making them into a movie. This is only available for Python 2.7 as of now.


Downloads
=========

In order to be able to run the conversions from the map images to movies, please download [ImageMagick](http://www.imagemagick.org/script/download.php). 
And note that if you want to be able to create a .mov file rather than a .gif, you must also have FFmpeg installed.

As well, you must have a gmail account because this uses the Google static maps API

Coming Soon
===========

I am going to be changing the code so that it is made up of 2 classes, Map and Analyze. Everything given already is the Map class, and Analyze will be methods of analyzing the GPS data. Two functions that will be available in the Analyze class are a home finder and movement watcher.

Documentation
=============

The full documentation is available above, but here is a snipit of how to create a map of one person moving given their coordinates.

first lets import it:

	import mappy as mp
	
in order to use MapPy, you are going to need a csv containing latitude and longitude, and, if you have it, time.

So lets say our csv contains all the GPS coordinates and relevant time for a single person from 1/1/13 to 4/1/13 for 5 hours a day (3 months of data) with latitude in the first column, longitude in the second, and datetime in the third (can be datetime object or string). The following code will separate them into lists:

	import csv
	reader = csv.reader(open('file_name.csv','rb'))
	header = reader.next()
	l = [row for row in reader]
	new_l = zip(*l)
	latitudes = list(new_l[0])
	longitudes = list(new_l[1])
	times = list(new_l[2])

now it's time to create our movie. First lets assign some variables:

	destination = 'directory/movies' #name of directory. This is crucial because all image files will be deleted from this directory after the process as to prevent compiling the wrong images
	name = 'example_movie' #Name of movie file without an extension
	first_day = '01-10-2013' #starting date for the data to grab
	last_day = '01-12-2013' #ending date for the data to grab
	sample_by = 'm5' #only grab data at a minimum interval of 5 minutes

now that we have set it so we don't end up grabbing 50,000 GPS coordinates, we can generate a map using the create_solo function:

	mp.create_solo(destination,name,latitudes,longitudes,times=times,start=first_day,end=last_day,by=sample_by)
	
there are many other keyword parameters that you can use to customize things like frames per second, the type of video, the size of the video, the label of the tick mark, and so on. In order to view the full documentation, click the documentation link in the repository.
