# Uncaptcha
Over pass google's recaptcha by using speech recognition method

## The Approach

unCaptcha2's approach is very simple:
1. Navigate to Google's ReCaptcha Demo site
2. Navigate to audio challenge for ReCaptcha
3. Download audio challenge
4. Submit audio challenge to Speech To Text
5. Parse response and type answer
6. Press submit and check if successful

## Version 0.1.2

## Setup
Run `setup.sh` script for installtion  
`DESTINATION` is the directory for programs to be
```
./setup.sh DESTINATION
```

## Preparation
Install program dependencies
```sh
pip3 install -r requirements.txt
```

Update coordinates value in `uncaptcha_config.ini` configuration file
```conf
# Example for [CURSOR] section
example-coords = x-pos, y-pos
# Example for [COLOR] section
example-color = #FFFFFF
```

## speech-to-text system 
**Default**  
`recognize_google`  

**Alternative**  
Settings in `queryAPI.py` file
- Google 
- Microsoft
- IBM


## Disclaimer
This repo is forked from [ecthros/uncaptcha2](https://github.com/ecthros/uncaptcha2) repository


## Version notes
**v0.1.2**
- Replace `os.system` usage with `subprocess` module
- Pre-check `ffmpeg` shell command

**v0.1.1**
- Close firefox browser window after each run
- Isolate configuration file
- Change naming convention style: Guido's recommendation


