# -*- conding: UTF-8 -*-

# Standard library imports
import configparser

class Config():

    def __init__(self, candidates):
        """
        Input:
            candidates - ini config files list
        Error Code:
            1 - No config ini file found
            3 - CONFIG section not exist
            5 - DEFAULT section not exist
            11 - Some needed key not exist in ini files
        """
        # self.HOME = str(pathlib.Path.home())

        # Sections 
        self.FILE_SEC = 'FILE'
        self.CURSOR_SEC = 'CURSOR'
        self.COLOR_SEC = 'COLOR'

        # Keys
        self.DOWNLOAD_LOCATION = 'download-location'

        self.PRIVATE_BROWSER = 'private-browser'
        self.SEARCH_COORDS = 'search-coords'
        self.GOOGLE_LOCATION = 'google-location'
        self.CAPTCHA_COORDS = 'captcha-coords'
        self.CHECK_COORDS = 'check-coords'
        self.AUDIO_COORDS = 'audio-coords'
        self.DOWNLOAD_COORDS = 'download-coords'
        self.FINAL_COORDS = 'final-coords'
        self.VERIFY_COORDS = 'verify-coords'
        self.CLOSE_LOCATION = 'close-location'

        self.PRIVATE_COLOR = 'private-color'
        self.GOOGLE_COLOR = 'google-color'
        self.CHECK_COLOR = 'check-color'

        # Get config information
        self._config = configparser.ConfigParser()
        self._config_found = self._config.read(candidates)

        # Make sure ini file exist
        if len(self._config_found) == 0:
            raise ConfigNotFoundError(configError)


    def download_location(self):
        """
        Return config DOWNLOAD_LOCATION option in FILE section
        """
        return self._read_value(self.FILE_SEC, self.DOWNLOAD_LOCATION)

    def private_browser(self):
        """
        Return config PRIVATE_BROWSER option in CURSOR section
        """
        return self._read_value(self.CURSOR_SEC, self.PRIVATE_BROWSER)

    def search_coords(self):
        """
        Return config SEARCH_COORDS option in CURSOR section
        """
        return self._read_value(self.CURSOR_SEC, self.SEARCH_COORDS)

    def google_location(self):
        """
        Return config GOOGLE_LOCATION option in CURSOR section
        """
        return self._read_value(self.CURSOR_SEC, self.GOOGLE_LOCATION)

    def captcha_coords(self):
        """
        Return config CAPTCHA_COORDS option in CURSOR section
        """
        return self._read_value(self.CURSOR_SEC, self.CAPTCHA_COORDS)

    def check_coords(self):
        """
        Return config CHECK_COORDS option in CURSOR section
        """
        return self._read_value(self.CURSOR_SEC, self.CHECK_COORDS)

    def audio_coords(self):
        """
        Return config AUDIO_COORDS option in CURSOR section
        """
        return self._read_value(self.CURSOR_SEC, self.AUDIO_COORDS)

    def download_coords(self):
        """
        Return config DOWNLOAD_COORDS option in CURSOR section
        """
        return self._read_value(self.CURSOR_SEC, self.DOWNLOAD_COORDS)

    def final_coords(self):
        """
        Return config FINAL_COORDS option in CURSOR section
        """
        return self._read_value(self.CURSOR_SEC, self.FINAL_COORDS)

    def verify_coords(self):
        """
        Return config VERIFY_COORDS option in CURSOR section
        """
        return self._read_value(self.CURSOR_SEC, self.VERIFY_COORDS)

    def close_location(self):
        """
        Return config CLOSE_LOCATION option in CURSOR section
        """
        return self._read_value(self.CURSOR_SEC, self.CLOSE_LOCATION)

    def private_color(self):
        """
        Return config PRIVATE_COLOR option in COLOR section
        """
        return self._read_value(self.COLOR_SEC, self.PRIVATE_COLOR)

    def google_color(self):
        """
        Return config GOOGLE_COLOR option in COLOR section
        """
        return self._read_value(self.COLOR_SEC, self.GOOGLE_COLOR)

    def check_color(self):
        """
        Return config CHECK_COLOR option in COLOR section
        """
        return self._read_value(self.COLOR_SEC, self.CHECK_COLOR)

    
    def _read_value(self, section, key):
        """
        Get the value of key inside section
        Input:
            section - config file section
            key - config file option
        Return:
            key value
        Error:
            NoSectionError - Section not found
            NoOptionError - Option not found
        """
        try:
            _config_value = self._config.get(section, key)
        except configparser.NoSectionError as error:
            raise NoSectionError(error)
        except configparser.NoOptionError as error:
            raise NoOptionError(error)
        else:
            return _config_value



# Exceptions
class configError(Exception):
    """
    Base class of config exception
    """
    pass

class ConfigNotFoundError(configError):
    """
    Raised if not finding ini file
    """
    pass

class NoSectionError(configError):
    """
    Raised by configparser.NoSectionError
    """
    pass

class NoOptionError(configError):
    """
    Raised by configparser.NoOptionError
    """