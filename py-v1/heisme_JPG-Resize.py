#-*- coding:utf-8 -*-
'''
	Heisme Image Resizer For Python Script

	jpg 이미지 리사이즈

	Tabsize : 4

	Version History
	v1.0    최초 작성

'''


import sys
import os
import getopt

# Global Variables

g_flagHelp = True
g_flagDebug = False
g_flagOverWrite = False

g_inputFolder = ""
g_inputFileExt = ".jpg"
g_dirSep = "\\"

g_outputSubFolder = ""
g_outputRes = ""
g_outputJpgQuality = 85

g_res = {
	# 가로형, 세로형, 정방형 각각 넓이만 정의함
	"300"   : (300, 200, 250),
	"400"   : (400, 250, 350),
	"500"   : (500, 350, 400),
	"600"   : (600, 400, 500),
	"640"   : (640, 420, 550),
	"700"   : (700, 450, 600),
	"800"   : (800, 550, 640),
	"900"   : (900, 600, 750),
	"1000"  : (1000, 650, 800),
	"1024"  : (1024, 700, 800),
	"1200"  : (1200, 800, 1000),
	"1400"  : (1400, 900, 1200),
	"1500"  : (1500, 1000, 1300),
	"2000"  : (2000, 1400, 1700),
}

# [0] min, [1] max
g_ratioSQ = (0.9, 1.1)

# Functions
def help ():

	exe_file = os.path.basename (sys.argv[0])

	help_message = exe_file + " -i INPUT_FULLPATH -r RESOLUTION [-o OUTPUT_SUBPATH -q QUALITY -h -v -f]\n\n" + \
		"-i INPUT_FULLPATH  Input Folder\n"  + \
		"-o OUTPUT_SUBPATH  Output SubFolder (Append INPUT FULLPATH) Default: res-RESOLUTION\n"  + \
		"-r RESOLUTION      Resolution set\n"  + \
		"                   (Horizontal, Vertical, Square)\n"

	for k in g_res.keys():
		help_message += \
		"                   H: " + str(g_res.get(k)[0]) + ", V: " + str(g_res.get(k)[1]) + ", SQ: " + str(g_res.get(k)[2]) + "\n"

	help_message += "\n" + \
		"-q QUALITY         Saved JPG Quality (10 ~ 95) Default : 85\n"  + \
		"-h                 Help Message\n"  + \
		"-v                 Verbose Mode\n"  + \
		"-f                 Force Write (Overwrite)\n"

	help_message += "\n: Square Ratio : " + str(g_ratioSQ[0]) + " ~ " + str(g_ratioSQ[1]) + "\n"

	print (help_message)
	return


def printStr (agStr) :
	print (agStr)

def debugPrint (agStr) :
	global g_flagDebug

	if g_flagDebug : print ("Debug : " + agStr)

import  pathlib
import  math
from    PIL     import  Image

def Process_Image_Resize (ag_full_filename, ag_outputSubFolder, ag_resPair) :

	global g_dirSep, g_overWrite, g_outputJpgQuality

	rt = 0

	debugPrint ("JPG Quality Check %d" % g_outputJpgQuality)
	if (g_outputJpgQuality < 10) or (g_outputJpgQuality > 95) :
		printStr ("JPG Quality Error %d" % g_outputJpgQuality)
		return 9


	debugPrint ("File Exist Check " + ag_full_filename)
	if os.path.isfile(ag_full_filename) == False:
		printStr ("File : " + ag_full_filename + " Not Exist")
		return 1

	srcPath, srcFilename = os.path.split(ag_full_filename)
	targetPath = srcPath + g_dirSep + ag_outputSubFolder
	debugPrint ("Folder Exist, Write Check " + targetPath)
	if os.path.exists(targetPath) == False :
		debugPrint ("Folder not Exist, mkdir " + targetPath)
		pathlib.Path(targetPath).mkdir(parents=True, exist_ok=True)

	targetFullFilename = targetPath + g_dirSep + srcFilename
	debugPrint ("Target Filename " + targetFullFilename)

	printStr ("File : " + ag_full_filename)
	printStr ("Output Folder : " + targetPath)


	# Target File Exist Check
	if  os.path.isfile(targetFullFilename) == True :
		if (g_overWrite == True) :
			printStr ("OverWrite!")
		else :
			printStr ("File : " + targetFullFilename + " Exist. Do not Process!")
			return 2

	with Image.open(ag_full_filename) as srcImg:
		srcWidth, srcHeight = srcImg.size
		debugPrint ("SrcImg Size %d x %d" % (srcWidth, srcHeight) )
		if (srcWidth <= 0) or (srcHeight <= 0) :
			debugPrint ("Image File Size Error")
			return 11

		# 0 : 가로형, 1: 세로형, 2: 정방형
		img_direct_str = ("Horizontal", "Vertical", "Square")
		b_img_direct = 3
		tmpVar = srcHeight / srcWidth
		if (tmpVar > g_ratioSQ[0]) and (tmpVar < g_ratioSQ[1]) :
			b_img_direct = 2
		else :
			if (srcWidth > srcHeight ) : b_img_direct = 0
			if (srcWidth < srcHeight ) : b_img_direct = 1

		if (b_img_direct <0) or (b_img_direct > 2) :
			debugPrint ("Image Direction Error %d" % b_img_direct)
			return 12

		printStr ("Image Direction %s" % img_direct_str[b_img_direct])

		#현재 사이즈와 목표 사이즈가 다를때만 처리
		to_maxWidth = ag_resPair[b_img_direct]
		if (to_maxWidth >= srcWidth) :
			debugPrint ("Don't Need Resize : org=%d dest=%d" % (srcWidth, to_maxWidth) )
			return 20

		newSize = to_maxWidth , math.ceil( to_maxWidth * ( srcHeight / srcWidth ) )


		printStr ("SrcFile : %d x %d" %(srcWidth, srcHeight) )
		printStr ("DestFile : %d x %d , Quality: %d" %(newSize[0], newSize[1], g_outputJpgQuality) )

		srcImg.thumbnail (newSize, Image.ANTIALIAS)
		srcImg.save(targetFullFilename, "JPEG", quality=g_outputJpgQuality)


	printStr ("----------- [Done] -----------")
	debugPrint ("Generate Resize Image " + g_outputSubFolder)


# Start Of Main
import configparser
def main():

	global  g_flagHelp, g_flagDebug, g_overWrite
	global  g_inputFolder, g_inputFileExt
	global  g_outputSubFolder
	global  g_outputRes, g_outputJpgQuality


	#ini File Read
	exePathFile, exeExt = os.path.splitext (sys.argv[0])
	iniFile = exePathFile + ".ini"
	sectionMain = "Main"
	
	config = configparser.ConfigParser ()  # ConfigParser모듈의 객체를 넣을 변수
	if config.read (iniFile) :
		g_flagDebug = config.getboolean (sectionMain, 'Verbose', fallback=False)
		g_overWrite = config.getboolean (sectionMain, 'OverWrite', fallback=True)
		g_outputJpgQuality = config.getint (sectionMain, 'Quality', fallback=85)
		g_outputRes = config.get (sectionMain, 'Resolution', fallback='1200')
		g_outputSubFolder = config.get (sectionMain, 'OutputSubFolder', fallback=('res-'+g_outputRes))
		g_inputFolder = config.get (sectionMain, 'InputFolder', fallback='')

	try:
		# 여기서 입력을 인자를 받는 파라미터는 단일문자일 경우 ':' 긴문자일경우 '='을끝에 붙여주면됨
		opts, args = getopt.getopt(sys.argv[1:],"hvfq:r:i:o:",["input=","output=","help"])
	except getopt.GetoptError as err:
		print (str(err))
		help()
		sys.exit(1)

	flagHelpSet = False
	
	for opt,arg in opts:
		if ( opt == "-h") or ( opt == "--help"):
			g_flagHelp = True
			flagHelpSet = True
		elif ( opt == "-v"):
			g_flagDebug = True
		elif ( opt == "-f"):
			g_overWrite = True
		elif ( opt == "-q" ) or ( opt == "--quality"):
			g_outputJpgQuality = int (arg)
		elif ( opt == "-i" ) or ( opt == "--input"):
			g_inputFolder = arg
		elif ( opt == "-o" ) or ( opt == "--output"):
			g_outputSubFolder = arg
		elif ( opt == "-r") or ( opt == "--res"):
			g_outputRes = arg

	if (flagHelpSet):
		help()
		sys.exit(0)

	# check Option
	if (g_inputFolder != "") and (g_outputRes != ""):
		g_flagHelp = False

	if (g_flagHelp):
		help()
		sys.exit(0)

	resPair = g_res.get (g_outputRes)
	if (resPair == None):
		printStr ("Res Key does not exist : " + g_outputRes)

	if (g_outputSubFolder == "") :
		g_outputSubFolder = "res-" + str(resPair[0])

	# Folder Check
	debugPrint ("Folder Exist " + g_inputFolder)
	if os.path.isdir (g_inputFolder) == False :
		printStr ("Folder " + g_inputFolder + " does not exist")
		sys.exit(0)

	debugPrint ("Folder Explorer With " + g_inputFileExt)
	filenames = os.listdir (g_inputFolder)

	#ini File Write
	if not config.has_section (sectionMain) : config.add_section (sectionMain)
	config.set (sectionMain, 'Verbose', str(g_flagDebug))
	config.set (sectionMain, 'OverWrite', str(g_overWrite))
	config.set (sectionMain, 'Quality', str(g_outputJpgQuality))
	config.set (sectionMain, 'Resolution', g_outputRes)
	config.set (sectionMain, 'OutputSubFolder', g_outputSubFolder)
	config.set (sectionMain, 'InputFolder', g_inputFolder)

	cfgfile = open (iniFile,'w')
	config.write(cfgfile)
	cfgfile.close()

	
	for fn in filenames :
		full_filename = os.path.join (g_inputFolder, fn)

		debugPrint ("Check " + full_filename)

		if os.path.isdir (full_filename) : continue

		ext = os.path.splitext (full_filename)[-1]

		if ext == g_inputFileExt:
			debugPrint ("Processing " + full_filename)
			rt = Process_Image_Resize (full_filename, g_outputSubFolder, resPair)

	return

# end Of Main

# Start
if __name__ == '__main__':
	main()

# End