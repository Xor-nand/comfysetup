# Copyright (C) 2017  The Comfysetup Authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import os
import subprocess
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s | %(levelname)s: %(message)s',
                    filename='comfy.log')
logger = logging.getLogger(__name__)
hdlr = logging.StreamHandler(sys.stdout)
hdlr.setLevel(logging.INFO)
hdlr.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(hdlr)


def check_updates():
    logger.info('Checking for updates...')
    os.chdir(os.environ['COMFY'])
    res = subprocess.check_output('./check_updates.sh')
    if type(res) == bytes:  res = res.decode().strip()
    logger.debug(res)
    if res == 'need to pull':
        close = False
        while not close:
            inp = input('There are updates available to Comfy. '
                        'Would you like to upgrade? [y/n]').lower()
            if inp == 'y':
                logger.info('Pulling upgrade... ')
                try:
                    out = subprocess.check_output('git pull').decode().strip()
                except subprocess.CalledProcessError:
                    logger.exception('An error occurred while '
                                     'performing upgrade.')
                else:
                    if 'up-to-date' or 'successful' in out:
                        logger.info('Successfully upgraded comfy.')
                close = True
            elif inp == 'n':
                close = True
            else:
                print("Please specify 'y' or 'n'.")
    elif res == 'up-to-date':
        logger.info('Comfy is up-to-date.')
    elif res == 'diverged':
        logger.warn('WARNING: you may have made changes to comfy that prevent '
                    'automatic updates. Please manually upgrade your '
                    'installation of Comfy.')


if __name__ == '__main__':
    logger.debug('Comfy started with args: {}'.format(sys.argv))
    if len(sys.argv) == 1:
        # GUI mode
        pass
    elif sys.argv[1] == '-Sy':
        # update list
        pass
    elif sys.argv[1] == '-Syu':
        # update list and upgrade cosmos
        pass
    else:
        # run package `sys.argv[1]`
        pass

    check_updates()