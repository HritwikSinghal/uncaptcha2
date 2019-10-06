# -*- coding: UTF-8 -*-

# Exit status:
#    1 - Usage error

# Standard library imports
import sys

# Third party library imports
# import third party libraries here

# Local application imports
from uncaptcha_pkg import uncaptcha_run 


def main():
    message = \
    """
    USAGE: 
        uncaptcha2.py run
        uncaptcha2.py setup 
    """

    if len(sys.argv) != 2:
        print(message)
        exit(1)
    elif sys.argv[1].lower() == 'run':
        uncaptcha_run.main()
    elif sys.argv[1].lower() == 'setup':
        # TODO: call uncaptcha package setup application
        pass
    else:
        print(message)
        exit(1)


if __name__ == '__main__':
    main()