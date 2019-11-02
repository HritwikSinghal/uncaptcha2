#!/bin/bash
#
# Program:
#   uncaptcha2 setup script
#
# Exit Code:
#   1 - Calling syntax error
#   3 - Destination directory does not exist
#
#   11 - Copy file failed
#   13 - Change file permission failed


# ============================
# Check exit code function
# USAGE:
#   checkCode EXITCODE MESSAGE
# ============================
function checkCode() {
  if [[ ${?} -ne 0 ]]; then
    echo ${2}
    exit ${1}
  fi
}

# ===========================
# Usage: Installation DESTDIR 
# ===========================
function Installation() {
    DESTDIR=${1}

    # Setup process
    cp README.md ${DESTDIR}
    checkCode 11 "Copy README.md failed." &> /dev/null
    cp uncaptcha2.py ${DESTDIR}
    checkCode 11 "Copy uncaptcha2.py failed."  &> /dev/null
    chmod 755 ${DESTDIR}/uncaptcha2.py
    checkCode 13 "Change file permission failed."   &> /dev/null

    if [[ ! -f ${DESTDIR}/uncaptcha_config.ini ]]; then
        cp uncaptcha_template.ini ${DESTDIR}/uncaptcha_config.ini
        checkCode 11 "Copy uncaptcha_template.ini failed."    &> /dev/null
        chmod 644 ${DESTDIR}/uncaptcha_config.ini
        checkCode 13 "Change file permission failed."
    fi

    cp requirements.txt ${DESTDIR}
    checkCode 11 "Copy requirements.txt failed." &> /dev/null
    cp -r uncaptcha_pkg ${DESTDIR}
    checkCode 11 "Copy uncaptcha_pkg directory failed." &> /dev/null
    cp -r uncaptcha_lib ${DESTDIR}
    checkCode 11 "Copy uncaptcha_lib directory failed" &> /dev/null
}


# Calling setup format check
USAGE="setup.sh DESTINATION"

if [[ "${#}" -ne 1 ]];  then
    echo -e "USAGE:\n    ${USAGE}"
    exit 1
fi

if [[ ! -d ${1} ]]; then
    echo "ERROR: Destination directory does not exist"
    exit 3
fi


# System checking
SYSTEM_RELEASE=$(uname -a)
case ${SYSTEM_RELEASE} in
  *Linux*)
    echo "Linux detected"
    echo ""
    Installation ${1}
    ;;
  *)
    echo "System not supported."
    exit 1
esac


echo "uncaptcha2 setup success."
exit 0
