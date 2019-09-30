# -*- coding: UTF-8 -*-

# Exit status:
#   11 - config.ConfigNotFoundError
#   12 - config.OptionFormatError
#   13 - shell command not found

# Standard library imports
import os
import subprocess
import time
import webbrowser

# Third party imports
import pyautogui
import speech_recognition as sr

# Local application imports
from uncaptcha_pkg import queryAPI
from uncaptcha_pkg import uncaptcha_conf 
# from queryAPI import bing, google, ibm


r = sr.Recognizer()


def run_command(command):
    ''' Run a command and get back its output '''
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    return proc.communicate()[0].split()[0]

def wait_for(coords, color):
    ''' Wait for a coordinate to become a certain color '''
    pyautogui.moveTo(coords)
    num_waited_for = 0

    test_color_rgb = pyautogui.screenshot().getpixel(coords)
    test_color = '#{:02x}{:02x}{:02x}'.format(test_color_rgb[0], test_color_rgb[1], test_color_rgb[2])
    while color.lower() != test_color.lower():
        time.sleep(.5)
        test_color_rgb = pyautogui.screenshot().getpixel(coords)
        test_color = '#{:02x}{:02x}{:02x}'.format(test_color_rgb[0], test_color_rgb[1], test_color_rgb[2])
        num_waited_for += 1
        if num_waited_for > 25:
            return -1
    return 0

def download_captcha(config):
    ''' Navigate to demo site, input user info, and download a captcha. '''
    print("Opening Firefox...")
    webbrowser.get('firefox').open_new_tab('https://www.google.com')
    time.sleep(1.5)
    pyautogui.hotkey('ctrl', 'shift', 'p')

    # if wait_for(PRIVATE_BROWSER, PRIVATE_COLOR) == -1: # Wait for browser to load
    if wait_for(config.private_browser_coords(), config.private_color()) == -1: # Wait for browser to load
        return -1
    
    print("Visiting Demo Site...")
    pyautogui.moveTo(config.search_coords())
    pyautogui.click()
    pyautogui.typewrite('https://www.google.com/recaptcha/api2/demo', interval=0.05)
    pyautogui.press('enter')
    time.sleep(.5)
    # Check if the page is loaded...
    pyautogui.moveTo(config.google_coords())
    if wait_for(config.google_coords(), config.google_color()) == -1: # Waiting for site to load
        return -1
    print("Get recaptcha demo page")

    print("Downloading Captcha...")
    pyautogui.moveTo(config.captcha_coords())
    pyautogui.click()
    time.sleep(5)
    test_color_rgb = pyautogui.screenshot().getpixel(config.check_coords())
    test_color = '#{:02x}{:02x}{:02x}'.format(test_color_rgb[0], test_color_rgb[1], test_color_rgb[2])
    if config.check_color().lower() == test_color.lower(): 
        print ("Already completed captcha.")
        return 2
    pyautogui.moveTo(config.audio_coords())
    pyautogui.click()
    time.sleep(2)
    pyautogui.moveTo(config.download_coords())
    pyautogui.click()
    time.sleep(3)
    
    pyautogui.hotkey('ctrl', 's')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'w')

    return 0

def check_captcha(config):
    ''' Check if we've completed the captcha successfully. '''
    pyautogui.moveTo(config.check_coords())
    test_color_rgb = pyautogui.screenshot().getpixel(config.check_coords())
    test_color = '#{:02x}{:02x}{:02x}'.format(test_color_rgb[0], test_color_rgb[1], test_color_rgb[2])
    if config.check_color().lower() == test_color.lower(): 
        print ("Successfully completed captcha.")
        output = 1
    else:
        print("An error occured.")
        output = 0
    pyautogui.moveTo(config.close_coords())
    pyautogui.click()
    return output

def run_cap(config):
    download_dir = config.download_location()

    try:
        print("Removing old files...")
        # These files may be left over from previous runs, and should be removed just in case.
        subprocess.Popen(['rm', download_dir + '/audio.wav'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        subprocess.Popen(['rm', download_dir + '/audio.mp3'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # First, download the file
        download_result = download_captcha(config)
        if download_result == 2:
            pyautogui.moveTo(config.close_coords())
            pyautogui.click()
            return 2
        elif download_result == -1:
            pyautogui.moveTo(config.close_coords())
            pyautogui.click()
            return 3
        print("Audio downloaded")
        
        # Convert the file to a format our APIs will understand
        print("Converting Captcha...")
        echo_process = subprocess.Popen(['echo', 'y'], stdout=subprocess.PIPE)
        ffmpeg_process = subprocess.Popen(['ffmpeg', '-i', download_dir + '/audio.mp3', download_dir + '/audio.wav'], 
            stdin=echo_process.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ffmpeg_process.wait()

        print('Reading audio file...')
        with sr.AudioFile(download_dir + '/audio.wav') as source:
            audio = r.record(source)

        print("Submitting To Speech to Text:")
        determined = queryAPI.google(audio) # Instead of google, you can use ibm or bing here
        print(determined)

        print("Inputting Answer...")
        # Input the captcha 
        pyautogui.moveTo(config.final_coords())
        pyautogui.click()
        time.sleep(.5)
        pyautogui.typewrite(determined, interval=.03)
        time.sleep(.5)
        pyautogui.moveTo(config.verify_coords())
        pyautogui.click()

        print("Verifying Answer...")
        time.sleep(2)
        # Check that the captcha is completed
        result = check_captcha(config)
        return result
    except Exception as e:
        print(e)
        pyautogui.moveTo(config.close_coords())
        pyautogui.click()
        return 3


if __name__ == '__main__':
    
    # Test all config data
    try:
        config_data = uncaptcha_conf.Config(['uncaptcha_config.ini'])
    except uncaptcha_conf.ConfigNotFoundError as error:
       print(error)
       exit(11)

    try:
        config_data.validate()
    except uncaptcha_conf.OptionFormatError as error:
        print(error.message)
        exit(12)

    # Test script command
    ffmpeg_process = subprocess.Popen(['which', 'ffmpeg'], stdout=subprocess.PIPE)
    ffmpeg_process.poll()
    if ffmpeg_process.returncode:
        print('No ffmpeg shell command found, please install before execute program')
        exit(13)

    # Run this and print statistics
    success = 0
    fail = 0
    allowed = 0

    for _count in range(1):
        res = run_cap(config_data)
        if res == 1:
            success += 1
        elif res == 2: # Sometimes google just lets us in
            allowed += 1
        else:
            fail += 1

        print("SUCCESSES: " + str(success) + " FAILURES: " + str(fail) + " Allowed: " + str(allowed))
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'w')
