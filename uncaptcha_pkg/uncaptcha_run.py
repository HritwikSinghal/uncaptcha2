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


def main():
    """
    Executed and run uncaptcha2 when called:
        
        uncaptcha2.py run
    """
    
    # Test all config data
    try:
        config_data = uncaptcha_conf.Config(['uncaptcha_config.ini'])
    except uncaptcha_conf.ConfigNotFoundError as error:
        print(error)
        exit(11)

    # try:
    #     config_data.validate()
    # except uncaptcha_conf.OptionFormatError as error:
    #     print(error.message)
    #     exit(12)

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


def run_command(command):
    ''' Run a command and get back its output '''
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    return proc.communicate()[0].split()[0]

def wait_for(coords, color):
    ''' 
    Wait for a coordinate to become a certain color 
    Planned to be subtitued by function [wait_or_image]
    '''
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

def wait_for_image(image_path, wait_limits):
    """
    Wait for locating image on screen 
    
    Param
    - image_path: path of image
    - wait_limits: loop times limit
    Return
    - if image found:
        4-integer tuple (left, top, width, height)
    - if not found:
        string 'locate failed'
    """
    _tmp_image = './uncaptcha_lib/tmp/screenshot.png'
    
    num_waited_for = 0
    locate_image = None
    
    # locate_image = pyautogui.locateOnScreen(image_path)
    while locate_image == None:
        time.sleep(.5)
        # locate_image = pyautogui.locateOnScreen(image_path)
        pyautogui.screenshot(_tmp_image)
        locate_image = pyautogui.locate(image_path, _tmp_image)
        num_waited_for += 1
        if num_waited_for > wait_limits:
            return 'locate failed'
    return locate_image

# def calc_coords(image_path):
#     """
#     Calculate middle point of given image on screen
    
#     Return
#         Success: tuple - (x-coords, y-coords)
#         Failed: string 'locate failed'
#     """
#     image_info = wait_for_image(image_path, wait_limits=4)
    
#     if image_info == 'locate failed':
#         return image_info
#     else:
#         left_coords, top_coords, width, height = image_info
    
#     ret_coords = (left_coords + (width // 2), top_coords + (height // 2))
#     return ret_coords


def download_captcha(config):
    ''' Navigate to demo site, input user info, and download a captcha. '''
    print("Opening Firefox...")
    webbrowser.get('firefox').open_new_tab('https://www.google.com')
    time.sleep(1.5)
    pyautogui.hotkey('ctrl', 'shift', 'p')
    time.sleep(2)
    pyautogui.press('f11')

    # if wait_for(config.private_browser_coords(), config.private_color()) == -1: # Wait for browser to load
    #     return -1
    # time.sleep(3)
    print('Private browser image: {}'.format(config.private_browser_img()))
    if wait_for_image(config.private_browser_img(), wait_limits=20) == 'locate failed':
        return -1
    
    print("Visiting Demo Site...")
    # pyautogui.moveTo(config.search_coords())
    # pyautogui.click()
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.typewrite('https://www.google.com/recaptcha/api2/demo', interval=0.05)
    pyautogui.press('enter')
    time.sleep(.5)
    # Check if the page is loaded...
    # pyautogui.moveTo(config.google_coords())
    # if wait_for(config.google_coords(), config.google_color()) == -1: # Waiting for site to load
        # return -1
    print('Find tab_logo_img...')
    if wait_for_image(config.tab_logo_img(), wait_limits=20) == 'locate failed':
        return -1
    print("Get recaptcha demo page")

    print("Downloading Captcha...")
    # pyautogui.moveTo(config.captcha_coords())
    print('Find recaptcha_img...')
    
    # captcha_coords = calc_coords(config.recaptcha_img())
    captcha_coords = wait_for_image(config.recaptcha_img(), wait_limits=10)
    if captcha_coords == 'locate failed':
        return -1
    # pyautogui.moveTo(captcha_coords)
    captcha_coords = pyautogui.center(captcha_coords)
    pyautogui.click(captcha_coords)
    time.sleep(3)
    # test_color_rgb = pyautogui.screenshot().getpixel(config.check_coords())
    # test_color = '#{:02x}{:02x}{:02x}'.format(test_color_rgb[0], test_color_rgb[1], test_color_rgb[2])
    # if config.check_color().lower() == test_color.lower(): 
    #     print ("Already completed captcha.")
    #     return 2
    if wait_for_image(config.verify_check_img(), wait_limits=2) == 'locate failed':
        print('Find audio_coords... {}')

        # audio_coords = calc_coords(config.audio_button_img())
        # audio_coords = wait_for_image(config.audio_button_img(), wait_limits=10)
        # if audio_coords == 'locate failed':
            # print('locate audio button coordinate failed')
            # return -1
        # pyautogui.moveTo(config.audio_coords())
        # pyautogui.moveto(audio_coords)
        # audio_coords = pyautogui.center(audio_coords)
        # pyautogui.click(audio_coords)
        pyautogui.press('enter')
        time.sleep(2)

        # pyautogui.moveTo(config.download_coords())
        print('Find download_coords...')
        # download_coords = calc_coords(config.download_button_img())
        download_coords = wait_for_image(config.download_button_img(), wait_limits=10)
        if download_coords == 'locate failed':
            print('locate download button failed')
            return -1
        download_coords = pyautogui.center(download_coords)
        # pyautogui.moveto(download_coords)
        pyautogui.click(download_coords)
        time.sleep(3)
        
        pyautogui.hotkey('ctrl', 's')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.hotkey('ctrl', 'w')
    else:
        print('Already completed captcha')
        return 2

    return 0

def check_captcha(config):
    ''' Check if we've completed the captcha successfully. '''
    # pyautogui.moveTo(config.check_coords())
    # test_color_rgb = pyautogui.screenshot().getpixel(config.check_coords())
    # test_color = '#{:02x}{:02x}{:02x}'.format(test_color_rgb[0], test_color_rgb[1], test_color_rgb[2])
    if wait_for_image(config.verify_check_img(), wait_limits=20) == 'locate failed':
        print('An error occured.')
        output = 0
    else:
        print('Successfully completed captcha.')
        output = 1 
    # if config.check_color().lower() == test_coVlor.lower(): 
    #     print ("Successfully completed captcha.")
    #     output = 1
    # else:
    #     print("An error occured.")
    #    output = 0
    # pyautogui.moveTo(config.close_coords())
    # pyautogui.click()
    pyautogui.hotkey('ctrl', 'w')
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
            # pyautogui.moveTo(config.close_coords())
            # pyautogui.click()
            pyautogui.hotkey('ctrl', 'w')
            return 2
        elif download_result == -1:
            # pyautogui.moveTo(config.close_coords())
            # pyautogui.click()
            pyautogui.hotkey('ctrl', 'w')
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
        # pyautogui.moveTo(config.final_coords())
        # pyautogui.click()
        # ans_coords = calc_coords(config.insert_ans_img())
        # verify_coords = calc_coords(config.verify_button_img())
        pyautogui.moveTo(10,10)
        ans_coords = wait_for_image(config.insert_ans_img(), wait_limits=10)
        verify_coords = wait_for_image(config.verify_button_img(), wait_limits=10)
        if ans_coords == 'locate failed' or verify_coords == 'locate failed':
            print('Failed locating image (ans-insert or verify-button)')
            return 3
        ans_coords = pyautogui.center(ans_coords)
        verify_coords = pyautogui.center(verify_coords)
        # pyautogui.moveTo(ans_coords)
        pyautogui.click(ans_coords)
        time.sleep(.5)
        pyautogui.typewrite(determined, interval=.03)
        time.sleep(.5)
        # pyautogui.moveTo(config.verify_coords())
        pyautogui.click(verify_coords)

        print("Verifying Answer...")
        time.sleep(2)
        # Check that the captcha is completed
        result = check_captcha(config)
        return result
    except Exception as e:
        print(e)
        # pyautogui.moveTo(config.close_coords())
        # pyautogui.click()
        pyautogui.hotkey('ctrl', 'w')
        return 3


if __name__ == '__main__':
    main()
