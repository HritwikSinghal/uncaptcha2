import time
import pyautogui
import speech_recognition as sr
import os
import subprocess

import webbrowser

from queryAPI import bing, google, ibm

''' You'll need to update based on the coordinates of your setup (Home PC setup) '''
# FIREFOX_ICON_COORDS = (25, 	 67) # Location of the Firefox icon on the side toolbar (to left click)
# PRIVATE_COORDS		= (178,  69) # Location of "Open a new Private Window"
PRIVATE_BROWSER 	= (2210, 735) # A place where the background of the Private Window will be
PRIVATE_COLOR		= '#25003E'  # The color of the background of the Private Window
SEARCH_COORDS 		= (2498, 121) # Location of the Firefox Search box
# REFRESH_COORDS      = (181, 137) # Refresh button
GOOGLE_LOCATION     = (1937, 80) # Location of the Google Icon after navigating to google.com/recaptcha/api2/demo
GOOGLE_COLOR 		= '#EA4335'  # Color of the Google Icon
CAPTCHA_COORDS		= (1981, 531) # Coordinates of the empty CAPTCHA checkbox
CHECK_COORDS 		= (1979, 533) # Location where the green checkmark will be
CHECK_COLOR 		= '#009e55'  # Color of the green checkmark
AUDIO_COORDS		= (2082, 799) # Location of the Audio button
DOWNLOAD_COORDS		= (2146, 590) # Location of the Download button
FINAL_COORDS  		= (2128, 538) # Text entry box
VERIFY_COORDS 		= (2222, 649) # Verify button
CLOSE_LOCATION		= (3814, 54)

DOWNLOAD_LOCATION = "/home/haw/Downloads/"
''' END SETUP '''

''' You'll need to update based on the coordinates of your setup (Thinkpad setup) '''
# FIREFOX_ICON_COORDS = (25, 	 67) # Location of the Firefox icon on the side toolbar (to left click)
# PRIVATE_COORDS		= (178,  69) # Location of "Open a new Private Window"
# PRIVATE_BROWSER 	= (245, 745) # A place where the background of the Private Window will be
# PRIVATE_COLOR		= '#25003E'  # The color of the background of the Private Window
# SEARCH_COORDS 		= (342, 121) # Location of the Firefox Search box
# REFRESH_COORDS      = (181, 137) # Refresh button
# GOOGLE_LOCATION     = (17, 80) # Location of the Google Icon after navigating to google.com/recaptcha/api2/demo
# GOOGLE_COLOR 		= '#EA4335'  # Color of the Google Icon
# CAPTCHA_COORDS		= (154, 531) # Coordinates of the empty CAPTCHA checkbox
# CHECK_COORDS 		= (158, 542) # Location where the green checkmark will be
# CHECK_COLOR 		= '#35B178'  # Color of the green checkmark
# AUDIO_COORDS		= (258, 797) # Location of the Audio button
# DOWNLOAD_COORDS		= (318, 590) # Location of the Download button
# FINAL_COORDS  		= (315, 534) # Text entry box
# VERIFY_COORDS 		= (406, 647) # Verify button
# CLOSE_LOCATION		= (1095, 75)

# DOWNLOAD_LOCATION = "../Downloads/"
''' END SETUP '''

r = sr.Recognizer()

def runCommand(command):
	''' Run a command and get back its output '''
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	return proc.communicate()[0].split()[0]

def waitFor(coords, color):
	''' Wait for a coordinate to become a certain color '''
	pyautogui.moveTo(coords)
	numWaitedFor = 0

	test_color_rgb = pyautogui.screenshot().getpixel(coords)
	test_color = '#{:02x}{:02x}{:02x}'.format(test_color_rgb[0], test_color_rgb[1], test_color_rgb[2])
	while color.lower() != test_color.lower():
		time.sleep(.5)
		test_color_rgb = pyautogui.screenshot().getpixel(coords)
		test_color = '#{:02x}{:02x}{:02x}'.format(test_color_rgb[0], test_color_rgb[1], test_color_rgb[2])
		numWaitedFor += 1
		if numWaitedFor > 25:
			return -1
	return 0

def downloadCaptcha():
	''' Navigate to demo site, input user info, and download a captcha. '''
	print("Opening Firefox")
	webbrowser.get('firefox').open_new_tab('https://www.google.com')
	time.sleep(1.5)
	pyautogui.hotkey('ctrl', 'shift', 'p')
	# pyautogui.moveTo(FIREFOX_ICON_COORDS)
	# pyautogui.rightClick()
	# time.sleep(.3)
	# pyautogui.moveTo(PRIVATE_COORDS)
	# pyautogui.click()
	# time.sleep(.5)
	if waitFor(PRIVATE_BROWSER, PRIVATE_COLOR) == -1: # Wait for browser to load
		return -1
	
	print("Visiting Demo Site")
	pyautogui.moveTo(SEARCH_COORDS)
	pyautogui.click()
	pyautogui.typewrite('https://www.google.com/recaptcha/api2/demo', interval=0.05)
	pyautogui.press('enter')
	time.sleep(.5)
	# Check if the page is loaded...
	pyautogui.moveTo(GOOGLE_LOCATION)
	if waitFor(GOOGLE_LOCATION, GOOGLE_COLOR) == -1: # Waiting for site to load
		return -1
	print("Get recaptcha demo page")

	print("Downloading Captcha")
	pyautogui.moveTo(CAPTCHA_COORDS)
	pyautogui.click()
	time.sleep(5)
	# pyautogui.moveTo(CHECK_COORDS)
	# if CHECK_COLOR in runCommand("eval $(xdotool getmouselocation --shell); xwd -root -silent | convert xwd:- -depth 8 -crop \"1x1+$X+$Y\" txt:- | grep -om1 '#\w\+'"):
	test_color_rgb = pyautogui.screenshot().getpixel(CHECK_COORDS)
	test_color = '#{:02x}{:02x}{:02x}'.format(test_color_rgb[0], test_color_rgb[1], test_color_rgb[2])
	if CHECK_COLOR.lower() == test_color.lower(): 
		print ("Already completed captcha.")
		return 2
	pyautogui.moveTo(AUDIO_COORDS)
	pyautogui.click()
	time.sleep(2)
	pyautogui.moveTo(DOWNLOAD_COORDS)
	pyautogui.click()
	time.sleep(3)
	
	pyautogui.hotkey('ctrl', 's')
	time.sleep(0.5)
	pyautogui.press('enter')
	time.sleep(0.5)
	pyautogui.hotkey('ctrl', 'w')

	return 0

def checkCaptcha():
	''' Check if we've completed the captcha successfully. '''
	pyautogui.moveTo(CHECK_COORDS)
	test_color_rgb = pyautogui.screenshot().getpixel(CHECK_COORDS)
	test_color = '#{:02x}{:02x}{:02x}'.format(test_color_rgb[0], test_color_rgb[1], test_color_rgb[2])
	if CHECK_COLOR.lower() == test_color.lower(): 
	# if CHECK_COLOR in runCommand("eval $(xdotool getmouselocation --shell); xwd -root -silent | convert xwd:- -depth 8 -crop \"1x1+$X+$Y\" txt:- | grep -om1 '#\w\+'"):
		print ("Successfully completed captcha.")
		output = 1
	else:
		print("An error occured.")
		output = 0
	pyautogui.moveTo(CLOSE_LOCATION)
	pyautogui.click()
	return output

def runCap():
	try:
		print("Removing old files...")
		os.system('rm ' + DOWNLOAD_LOCATION + 'audio.wav 2>/dev/null') # These files may be left over from previous runs, and should be removed just in case.
		os.system('rm ' + DOWNLOAD_LOCATION + 'audio.mp3 2>/dev/null')
		# First, download the file
		downloadResult = downloadCaptcha()
		if downloadResult == 2:
			pyautogui.moveTo(CLOSE_LOCATION)
			pyautogui.click()
			return 2
		elif downloadResult == -1:
			pyautogui.moveTo(CLOSE_LOCATION)
			pyautogui.click()
			return 3
		print("Audio downloaded")
		
		# Convert the file to a format our APIs will understand
		print("Converting Captcha...")
		os.system("echo 'y' | ffmpeg -i " + DOWNLOAD_LOCATION + "audio.mp3 " + DOWNLOAD_LOCATION + "audio.wav 2>/dev/null")
		print('Reading audio file...')
		with sr.AudioFile(DOWNLOAD_LOCATION + 'audio.wav') as source:
			audio = r.record(source)

		print("Submitting To Speech to Text:")
		determined = google(audio) # Instead of google, you can use ibm or bing here
		print(determined)

		print("Inputting Answer")
		# Input the captcha 
		pyautogui.moveTo(FINAL_COORDS)
		pyautogui.click()
		time.sleep(.5)
		pyautogui.typewrite(determined, interval=.05)
		time.sleep(.5)
		pyautogui.moveTo(VERIFY_COORDS)
		pyautogui.click()

		print("Verifying Answer")
		time.sleep(2)
		# Check that the captcha is completed
		result = checkCaptcha()
		return result
	except Exception as e:
		print(e)
		pyautogui.moveTo(CLOSE_LOCATION)
		pyautogui.click()
		return 3


if __name__ == '__main__':
	success = 0
	fail = 0
	allowed = 0

	# Run this forever and print statistics
	# while True:
	for _count in range(3):
		res = runCap()
		if res == 1:
			success += 1
		elif res == 2: # Sometimes google just lets us in
			allowed += 1
		else:
			fail += 1

		print("SUCCESSES: " + str(success) + " FAILURES: " + str(fail) + " Allowed: " + str(allowed))
		pyautogui.moveTo(CLOSE_LOCATION)
		pyautogui.click()