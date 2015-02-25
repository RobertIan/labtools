import Tkinter, tkFileDialog
import os
import os.path
import time
from PIL import Image
from PIL.ExifTags import TAGS
from time import localtime, strftime
import subprocess
######################################
#If not working 1) make sure location of ffprobe.exe is correct...
######################################
#APPS#

class App:
	def get_exif(self, path): #retrieves EXIF info(image file metadata)
		print "Getting EXIF..."
		exifData = {}
		i = Image.open(str(path))
		info = i._getexif()
		for tag, value in info.items():
			decoded = TAGS.get(tag, tag)
			exifData[decoded] = value
		print "Writing EXIF..."
		f.write(root +"; " + file + "; " + time.ctime(os.path.getmtime(os.path.join(root,file))) + "; " + str(exifData['ISOSpeedRatings']) + "; " + str(exifData['FNumber']) + "; " + str(exifData['ExposureTime']) + "\n")
	def getVidInfo(self, path): #outputs video length and time info -- we do not have a module that does this just yet
		print "Getting Video Info..."
		result = subprocess.Popen(["C:\\FFMPEG\\ffprobe.exe", path], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
		for x in result.stdout.readlines():
		    if "Duration" in x:
			    Duration = x
		print "Writing Video Info..."
		f.write(root +"; " + file + "; " + time.ctime(os.path.getmtime(os.path.join(root,file))) + "; ; ; ; " + str(Duration))

		
		
######################################
#FILE DIALOG/EXTENSION TEST#

root = Tkinter.Tk()
root.withdraw()

dirname = tkFileDialog.askdirectory(parent=root,initialdir=r"C:/", title="Which folder would you like info for?")

appThinger = App()

if len(dirname) > 0:
    dirGuess = "fileList("+strftime("%m-%d-%Y %H.%M.%S", localtime())+").txt"
    f = open(os.path.join(r'C:\\Users\\Ian\\Desktop',dirGuess), 'w')
    print dirname
    path = dirname
    for root, dirs, files in os.walk(path):
        for file in files:
            filename, fileExtension = os.path.splitext(file)
            if (fileExtension == '.DUMP')or(fileExtension =='.dump'):
                f.write(root +"; " + file + "; " + time.ctime(os.path.getmtime(os.path.join(root,file))) + "No Other File Info on DUMP files" + "\n")
            elif (fileExtension =='.JPG')or(fileExtension =='.jpg'):
                fileAndDir=os.path.join(root,file)
                appThinger.get_exif(fileAndDir)
            elif (fileExtension == '.MP4')or(fileExtension == '.mp4')or(fileExtension == '.avi')or(fileExtension == '.AVI'):
                fileAndDir=os.path.join(root,file)
                appThinger.getVidInfo(fileAndDir)
            else:
                f.write(root + "; " + file + "; " + "Unrecognized File Type" + "\n")


